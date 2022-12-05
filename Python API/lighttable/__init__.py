from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from typing import Dict
import objc
from GlyphsApp import Glyphs, GSFont, GSGlyph, GSLayer

__all__ = [
    "Commit",
    "ComponentIntegrationPlan",
    "ComponentIntegrationStrategy",
    "DocumentState",
    "ObjectStatus",
    "Record",
    "RestorationInfo",
    "Signature",
    "Version",
]

Signature = objc.lookUpClass("LightTableSignature")
Commit = objc.lookUpClass("LightTableCommit")
Record = objc.lookUpClass("LightTableRecord")
Version = objc.lookUpClass("LightTableVersion")
RestorationInfo = objc.lookUpClass("LightTableRestorationInfo")
_ComponentIntegrationPlan = objc.lookUpClass("LightTableComponentIntegrationPlan")
_LightTableInterface = objc.lookUpClass("LightTableInterface")

objc.registerMetaDataForSelector(
    b"LightTableInterface",
    b"font:loadVersionForRecord:completionHandler:",
    {
        "retval": {"type": b"c"},
        "arguments": {
            2: {"type": b"@"},
            3: {"type": b"@"},
            4: {
                "callable": {
                    "retval": {"type": b"v"},
                    "arguments": {
                        0: {"type": b"^v"},
                        1: {"type": b"@"},
                        2: {"type": b"@"},
                    },
                }
            },
        },
    },
)

## GSFont

class DocumentState(Enum):
    UNKNOWN = 0
    NO_FILE = 1
    NO_REPOSITORY = 2
    ERROR = 3
    OPERATIONAL = 4

GSFont.lt_document_state = property(
    lambda self: DocumentState(_LightTableInterface.documentStateOfFont_(self))
)

GSFont.lt_selected_version = property(
    lambda self: _LightTableInterface.activeVersionOfFont_(self)
)

GSFont.lt_available_records = property(
    lambda self: _LightTableInterface.availableRecordsForFont_(self)
)

GSFont.lt_load_version = objc.python_method(
    lambda self, record, callback: _LightTableInterface.font_loadVersionForRecord_completionHandler_(
        self, record, callback
    )
)

GSFont.lt_glyph_changeset_of_record = objc.python_method(
    lambda self, record: _LightTableInterface.glyphChangesetOfRecord_inFont_(
        record, self
    )
)

## GSGlyph

class ObjectStatus(Enum):
    UNKNOWN = 0
    UNMODIFIED = 1
    ADDED = 2
    MODIFED = 3

GSGlyph.lt_status = property(lambda self: ObjectStatus(self.lightTableStatus()))

GSGlyph.lt_restoration_info = objc.python_method(
    lambda self: _LightTableInterface.restorationInfoForLayer_(self.layers[0])
)

## GSLayer

GSLayer.lt_status = property(lambda self: ObjectStatus(self.lightTableStatus()))

GSLayer.lt_restoration_info = objc.python_method(
    lambda self: _LightTableInterface.restorationInfoForLayer_(self)
)

## Signature

Signature.name = property(lambda self: self.pyobjc_instanceMethods.name())
Signature.email_address = property(
    lambda self: self.pyobjc_instanceMethods.emailAddress()
)
Signature.datetime = property(lambda self: self.pyobjc_instanceMethods.date())

## Commit

Commit.id = property(lambda self: self.pyobjc_instanceMethods.id())
Commit.summary = property(lambda self: self.pyobjc_instanceMethods.summary())
Commit.author = property(lambda self: self.pyobjc_instanceMethods.author())
Commit.committer = property(lambda self: self.pyobjc_instanceMethods.committer())

## Record

Record.commit = property(lambda self: self.pyobjc_instanceMethods.commit())
Record.filepath = property(lambda self: self.pyobjc_instanceMethods.filePath())

## Version

Version.font = property(lambda self: self.pyobjc_instanceMethods.font())
Version.record = property(lambda self: self.pyobjc_instanceMethods.record())

## Restoration Info

RestorationInfo.info_for = staticmethod(lambda element: element.lt_restoration_info)

RestorationInfo.base_layer = property(
    lambda self: self.pyobjc_instanceMethods.baseLayer()
)
RestorationInfo.base_glyph = property(
    lambda self: self.pyobjc_instanceMethods.baseGlyph()
)
RestorationInfo.base_font = property(
    lambda self: self.pyobjc_instanceMethods.baseFont()
)
RestorationInfo.restoration_layer = property(
    lambda self: self.pyobjc_instanceMethods.restorationLayer()
)
RestorationInfo.restoration_glyph = property(
    lambda self: self.pyobjc_instanceMethods.restorationGlyph()
)
RestorationInfo.restoration_font = property(
    lambda self: self.pyobjc_instanceMethods.restorationFont()
)


## Component Integration Plan


class ComponentIntegrationStrategy(Enum):
    USE_BASE_COMPONENT_GLYPH = 1
    INTEGRATE_COMPONENT_GLYPH = 2
    INTEGRATE_AS_PATHS = 3


@dataclass
class ComponentIntegrationPlan:
    strategies: Dict[str, ComponentIntegrationStrategy]
    fallback: ComponentIntegrationStrategy


def _resolve_component_integration_plan(
    plan: ComponentIntegrationPlan | ComponentIntegrationStrategy | None,
) -> _ComponentIntegrationPlan:  # type: ignore
    if plan is None:
        return _ComponentIntegrationPlan.planWithStrategies_fallbackStrategy_(
            {}, ComponentIntegrationStrategy.USE_BASE_COMPONENT_GLYPH.value
        )
    elif isinstance(plan, ComponentIntegrationStrategy):
        return _ComponentIntegrationPlan.planWithStrategies_fallbackStrategy_(
            {}, plan.value
        )
    else:
        return _ComponentIntegrationPlan.planWithStrategies_fallbackStrategy_(
            {k: v.value for k, v in plan.strategies.items()}, plan.fallback.value
        )


## Restore Glyph and Layer

RestorationInfo.restore_glyph_as_replacement = objc.python_method(
    lambda self, component_integration_plan=None: _LightTableInterface.restoreGlyphAsReplacement_componentIntegrationPlan_(
        self, _resolve_component_integration_plan(component_integration_plan)
    )
)
RestorationInfo.restore_glyph_as_alternative = objc.python_method(
    lambda self, component_integration_plan=None: _LightTableInterface.restoreGlyphAsAlternative_componentIntegrationPlan_(
        self, _resolve_component_integration_plan(component_integration_plan)
    )
)

RestorationInfo.restore_layer_as_replacement = objc.python_method(
    lambda self, component_integration_plan=None: _LightTableInterface.restoreLayerAsReplacement_componentIntegrationPlan_(
        self, _resolve_component_integration_plan(component_integration_plan)
    )
)
RestorationInfo.restore_layer_as_backup_layer = objc.python_method(
    lambda self, component_integration_plan=None: _LightTableInterface.restoreLayerAsBackupLayer_componentIntegrationPlan_(
        self, _resolve_component_integration_plan(component_integration_plan)
    )
)
RestorationInfo.restore_layer_as_background = objc.python_method(
    lambda self, component_integration_plan=None: _LightTableInterface.restoreLayerAsBackground_componentIntegrationPlan_(
        self, _resolve_component_integration_plan(component_integration_plan)
    )
)
