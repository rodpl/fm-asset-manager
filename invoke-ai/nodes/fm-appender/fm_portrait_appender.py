"""InvokeAI node for preparing Football Manager portrait assets."""

from invokeai.app.invocations.baseinvocation import (
    BaseInvocation,
    BaseInvocationOutput,
    InvocationContext,
    invocation,
    invocation_output,
)
from invokeai.app.invocations.fields import InputField, OutputField

from ._file_ops import move_asset


@invocation_output("fm_portrait_appender_output")
class FMPortraitAppenderOutput(BaseInvocationOutput):
    """Details about the saved Football Manager portrait."""

    saved_portrait_path: str = OutputField(
        description="Absolute path to the relocated portrait image."
    )
    fm_id: str = OutputField(description="Football Manager identifier used for naming.")


@invocation(
    "fm_portrait_appender",
    title="FM Portrait Appender",
    tags=["fm", "utility", "files"],
    category="utility",
    version="1.0.0",
)
class FMPortraitAppenderInvocation(BaseInvocation):
    """Move a generated portrait into the Football Manager graphics folder."""

    image_path: str = InputField(
        description="Absolute path to the generated portrait image on disk."
    )
    fm_id: str = InputField(
        title="FM Person ID",
        description="Football Manager unique identifier for the person portrait.",
    )
    fm_folder_path: str = InputField(
        title="FM Folder Path",
        description=(
            "Football Manager graphics folder that should receive the portrait "
            "image."
        ),
    )

    def invoke(self, context: InvocationContext) -> FMPortraitAppenderOutput:
        context.logger.info(
            "FM Portrait Appender invoked with image=%s, fm_id=%s, target=%s",
            self.image_path,
            self.fm_id,
            self.fm_folder_path,
        )

        destination = move_asset(
            source_path=self.image_path,
            destination_dir=self.fm_folder_path,
            dest_stem=self.fm_id,
        )

        context.logger.info("Portrait moved to %s", destination)

        return FMPortraitAppenderOutput(
            saved_portrait_path=str(destination),
            fm_id=self.fm_id,
        )
