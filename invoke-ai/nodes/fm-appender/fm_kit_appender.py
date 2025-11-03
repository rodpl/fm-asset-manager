"""InvokeAI node for preparing Football Manager kit assets."""

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


@invocation_output("fm_kit_appender_output")
class FMKitAppenderOutput(BaseInvocationOutput):
    """Details about the saved Football Manager kit images."""

    saved_home_kit_path: Optional[str] = OutputField(
        default=None,
        description="Absolute path to the relocated home kit image (if provided).",
    )
    saved_away_kit_path: Optional[str] = OutputField(
        default=None,
        description="Absolute path to the relocated away kit image (if provided).",
    )
    saved_third_kit_path: Optional[str] = OutputField(
        default=None,
        description="Absolute path to the relocated third kit image (if provided).",
    )
    football_manager_id: str = OutputField(
        description="Identifier used to name the kit files."
    )
    target_folder_path: str = OutputField(
        description="Destination directory used for the kit files."
    )


@invocation(
    "fm_kit_appender",
    title="FM Kit Appender",
    tags=["fm", "utility", "files"],
    category="utility",
    version="1.0.0",
)
class FMKitAppenderInvocation(BaseInvocation):
    """Move generated kit images into the Football Manager graphics folder."""

    home_kit_path: Optional[str] = InputField(
        default=None, description="Absolute path to the home kit image to move."
    )
    away_kit_path: Optional[str] = InputField(
        default=None, description="Absolute path to the away kit image to move."
    )
    third_kit_path: Optional[str] = InputField(
        default=None, description="Absolute path to the third kit image to move."
    )
    fm_id: str = InputField(
        title="FM Club ID",
        description="Football Manager unique identifier for the club kits.",
    )
    fm_folder_path: str = InputField(
        title="Kit Folder Path",
        description="Football Manager graphics folder that should receive the kits.",
    )

    def invoke(self, context: InvocationContext) -> FMKitAppenderOutput:
        context.logger.info(
            (
                "FM Kit Appender invoked with home=%s, away=%s, third=%s, "
                "fm_id=%s, target=%s"
            ),
            self.home_kit_path,
            self.away_kit_path,
            self.third_kit_path,
            self.fm_id,
            self.fm_folder_path,
        )

        if not any([self.home_kit_path, self.away_kit_path, self.third_kit_path]):
            raise ValueError("Provide at least one kit image path to move.")

        home_destination = move_optional_asset(
            source_path=self.home_kit_path,
            destination_dir=self.fm_folder_path,
            dest_stem=f"{self.fm_id}_kit_home",
        )
        away_destination = move_optional_asset(
            source_path=self.away_kit_path,
            destination_dir=self.fm_folder_path,
            dest_stem=f"{self.fm_id}_kit_away",
        )
        third_destination = move_optional_asset(
            source_path=self.third_kit_path,
            destination_dir=self.fm_folder_path,
            dest_stem=f"{self.fm_id}_kit_third",
        )

        if home_destination:
            context.logger.info("Home kit moved to %s", home_destination)
        if away_destination:
            context.logger.info("Away kit moved to %s", away_destination)
        if third_destination:
            context.logger.info("Third kit moved to %s", third_destination)

        return FMKitAppenderOutput(
            saved_home_kit_path=str(home_destination) if home_destination else None,
            saved_away_kit_path=str(away_destination) if away_destination else None,
            saved_third_kit_path=str(third_destination) if third_destination else None,
            football_manager_id=self.fm_id,
            target_folder_path=self.fm_folder_path,
        )
