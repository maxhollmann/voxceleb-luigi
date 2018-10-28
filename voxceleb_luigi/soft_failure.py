import traceback
import luigi

from .util import pipeline_path


class softly_failing:
    def __init__(self, catch_all=False, propagate=False):
        self._catch_all = catch_all
        self._propagate = propagate


    def __call__(_self, task):
        @luigi.task._task_wraps(task)
        class Wrapped(task):
            def run(self):
                if _self._propagate:
                    failed_deps = [t for t in self.deps() if t.failed_softly()]
                    if any(failed_deps):
                        msg = "Propagated soft failure from:\n\n{}".format(
                            "\n\n=========\n\n".join(
                                [t.output(failed=True)._propagated_failure_message_part() for t in failed_deps]))
                        self.fail_softly(msg)
                        return

                try:
                    super().run()
                except Exception as e:
                    if _self._catch_all:
                        self.fail_softly(e)
                    else:
                        raise


            def fail_softly(self, exception_or_msg="failed"):
                if isinstance(exception_or_msg, Exception):
                    msg = ''.join(traceback.format_exception(etype=type(exception_or_msg),
                                                             value=exception_or_msg,
                                                             tb=exception_or_msg.__traceback__))
                else:
                    msg = exception_or_msg

                with self.output(failed=True).open("w") as f:
                    f.write(msg)

            def failed_softly(self):
                return self.output(failed=True).exists()


            def complete(self):
                return super().complete() or self.failed_softly()

            def output(self, failed=False):
                if failed:
                    return SoftFailureTarget(self.task_id)
                else:
                    return super().output()


        return Wrapped


class SoftFailureTarget(luigi.LocalTarget):
    def __init__(self, task_id):
        self._task_id = task_id
        self._task_fam = task_id.split("_", 1)[0]
        path = pipeline_path('soft_failures', self._task_fam, self._task_id)
        super().__init__(path)


    def _propagated_failure_message_part(self):
        if self._propagated():
            upstream_id = self._propagated_from()
            part2 = SoftFailureTarget(upstream_id)._propagated_failure_message_part()
        else:
            part2 = "\n{}".format(self._content().strip())
        return "-> {}\n{}".format(self._task_id, part2)

    def _propagated(self):
        return self._content().startswith("Propagated soft failure from")

    def _propagated_from(self):
        return self._content().split("\n")[2][3:]

    def _content(self):
        with self.open('r') as f:
            return f.read()
