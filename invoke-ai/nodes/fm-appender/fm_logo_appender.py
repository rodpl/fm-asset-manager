"""InvokeAI node for preparing Football Manager logo assets."""

from typing import Optional

from invokeai.app.invocations.baseinvocation import (
    BaseInvocation,
    BaseInvocationOutput,
    InvocationContext,
    invocation,
    invocation_output,
)
from invokeai.app.invocations.fields import InputField, OutputField

from ._file_ops import move_optional_asset


@invocation_output("fm_logo_appender_output")
class FMLogoAppenderOutput(BaseInvocationOutput):
    """Details about the saved Football Manager logos."""

    saved_logo_path: Optional[str] = OutputField(
        default=None,
        description="Absolute path to the relocated standard logo image (if provided).",
    )
    saved_small_logo_path: Optional[str] = OutputField(
        default=None,
        description="Absolute path to the relocated small logo image (if provided).",
    )
    football_manager_id: str = OutputField(
        description="Identifier used to name the logo files."
    )
    target_folder_path: str = OutputField(
        description="Destination directory used for the logo files."
    )


@invocation(
    "fm_logo_appender",
    title="FM Logo Appender",
    tags=["fm", "utility", "files"],
    category="utility",
    version="1.0.0",
)
class FMLogoAppenderInvocation(BaseInvocation):
    """Move generated logos into the Football Manager graphics folder."""

    normal_logo_path: Optional[str] = InputField(
        default=None,
        description="Absolute path to the standard-sized logo to move.",
    )
    small_logo_path: Optional[str] = InputField(
        default=None,
        description="Absolute path to the small-sized logo to move.",
    )
    fm_id: str = InputField(
        title="FM Club ID",
        description="Football Manager unique identifier for the club logo.",
    )
    fm_folder_path: str = InputField(
        title="Logo Folder Path",
        description="Football Manager graphics folder that should receive the logos.",
    )

    def invoke(self, context: InvocationContext) -> FMLogoAppenderOutput:
        context.logger.info(
            f"FM Logo Appender invoked with normal_logo={self.normal_logo_path}, "
            f"small_logo={self.small_logo_path}, fm_id={self.fm_id}, "
            f"target={self.fm_folder_path}"
        )

        if not self.normal_logo_path and not self.small_logo_path:
            raise ValueError(
                "Provide at least one logo image path to move (normal or small)."
            )

        normal_destination = move_optional_asset(
            source_path=self.normal_logo_path,
            destination_dir=self.fm_folder_path,
            dest_stem=f"{self.fm_id}_logo",
        )
        small_destination = move_optional_asset(
            source_path=self.small_logo_path,
            destination_dir=self.fm_folder_path,
            dest_stem=f"{self.fm_id}_logo_small",
        )

        if normal_destination:
            context.logger.info(f"Standard logo moved to {normal_destination}")
        if small_destination:
            context.logger.info(f"Small logo moved to {small_destination}")

        return FMLogoAppenderOutput(
            saved_logo_path=str(normal_destination) if normal_destination else None,
            saved_small_logo_path=str(small_destination)
            if small_destination
            else None,
            football_manager_id=self.fm_id,
            target_folder_path=self.fm_folder_path,
        )
