from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from typing import Dict
import objc
from objc import python_method
from GlyphsApp import Glyphs, GSGlyph, GSLayer

__all__ = [
    "ComponentIntegrationPlan",
    "ComponentIntegrationStrategy",
    "RestorationInfo",
]

RestorationManager = objc.lookUpClass("LightTableRestorationManager")

RestorationInfo = objc.lookUpClass("LightTableRestorationInfo")


def _RestorationInfo_info_for(element: GSGlyph | GSLayer) -> RestorationInfo | None:
    if isinstance(element, GSGlyph):
        return RestorationManager.restorationInfoForLayer_(element.layers[0])
    elif isinstance(element, GSLayer):
        return RestorationManager.restorationInfoForLayer_(element)


RestorationInfo.info_for = staticmethod(_RestorationInfo_info_for)


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


class ComponentIntegrationStrategy(Enum):
    USE_BASE_COMPONENT_GLYPH = 1
    INTEGRATE_COMPONENT_GLYPH = 2
    INTEGRATE_AS_PATHS = 3


@dataclass
class ComponentIntegrationPlan:
    strategies: Dict[str, ComponentIntegrationStrategy]
    fallback: ComponentIntegrationStrategy


ObjcComponentIntegrationPlan = objc.lookUpClass("LightTableComponentIntegrationPlan")


def resolve_component_integration_plan(
    plan: ComponentIntegrationPlan | ComponentIntegrationStrategy | None,
) -> ObjcComponentIntegrationPlan:
    if plan is None:
        return ObjcComponentIntegrationPlan.planWithStrategies_fallbackStrategy_(
            {}, ComponentIntegrationStrategy.USE_BASE_COMPONENT_GLYPH.value
        )
    elif isinstance(plan, ComponentIntegrationStrategy):
        return ObjcComponentIntegrationPlan.planWithStrategies_fallbackStrategy_(
            {}, plan.value
        )
    else:
        return ObjcComponentIntegrationPlan.planWithStrategies_fallbackStrategy_(
            {k: v.value for k, v in plan.strategies.items()}, plan.fallback.value
        )


def _RestorationInfo_restore_glyph_as_replacement(
    info: RestorationInfo,
    component_integration_plan: ComponentIntegrationPlan
    | ComponentIntegrationStrategy
    | None = None,
) -> GSLayer | None:
    return RestorationManager.restoreGlyphAsReplacement_componentIntegrationPlan_(
        info, resolve_component_integration_plan(component_integration_plan)
    )


RestorationInfo.restore_glyph_as_replacement = python_method(
    _RestorationInfo_restore_glyph_as_replacement
)


def _RestorationInfo_restore_glyph_as_alternative(
    info: RestorationInfo,
    component_integration_plan: ComponentIntegrationPlan
    | ComponentIntegrationStrategy
    | None = None,
) -> GSLayer | None:
    return RestorationManager.restoreGlyphAsAlternative_componentIntegrationPlan_(
        info, resolve_component_integration_plan(component_integration_plan)
    )


RestorationInfo.restore_glyph_as_alternative = python_method(
    _RestorationInfo_restore_glyph_as_alternative
)


def _RestorationInfo_restore_layer_as_replacement(
    info: RestorationInfo,
    component_integration_plan: ComponentIntegrationPlan
    | ComponentIntegrationStrategy
    | None = None,
) -> GSLayer | None:
    return RestorationManager.restoreLayerAsReplacement_componentIntegrationPlan_(
        info, resolve_component_integration_plan(component_integration_plan)
    )


RestorationInfo.restore_layer_as_replacement = python_method(
    _RestorationInfo_restore_layer_as_replacement
)


def _RestorationInfo_restore_layer_as_backup_layer(
    info: RestorationInfo,
    component_integration_plan: ComponentIntegrationPlan
    | ComponentIntegrationStrategy
    | None = None,
) -> GSLayer | None:
    return RestorationManager.restoreLayerAsBackupLayer_componentIntegrationPlan_(
        info, resolve_component_integration_plan(component_integration_plan)
    )


RestorationInfo.restore_layer_as_backup_layer = python_method(
    _RestorationInfo_restore_layer_as_backup_layer
)


def _RestorationInfo_restore_layer_as_background(
    info: RestorationInfo,
    component_integration_plan: ComponentIntegrationPlan
    | ComponentIntegrationStrategy
    | None = None,
) -> GSLayer | None:
    return RestorationManager.restoreLayerAsBackground_componentIntegrationPlan_(
        info, resolve_component_integration_plan(component_integration_plan)
    )


RestorationInfo.restore_layer_as_background = python_method(
    _RestorationInfo_restore_layer_as_background
)
