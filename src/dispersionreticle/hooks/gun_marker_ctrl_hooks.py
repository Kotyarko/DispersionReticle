from AvatarInputHandler import gun_marker_ctrl
from AvatarInputHandler.gun_marker_ctrl import _GunMarkersDPFactory, _MARKER_TYPE

from dispersionreticle.config import g_config
from dispersionreticle.controllers.gun_marker_decorator import NewGunMarkersDecorator
from dispersionreticle.controllers.gun_marker_default_controller import \
    NewDefaultGunMarkerController, \
    FocusGunMarkerController
from dispersionreticle.controllers.gun_marker_spg_controller import \
    NewSPGGunMarkerController, \
    FocusSPGGunMarkerController
from dispersionreticle.utils import *
from dispersionreticle.utils.reticle_registry import ReticleRegistry


###########################################################
# Return new decorator that includes new reticle controllers
#
# Basically, creates controllers of each markerType and provides them with proper
# data provider to communicate with crosshair flash component.
#
# Gun marker decorator manages all created controllers and forwards properly all methods
# related with them. Because decorator accepts only 2 controllers (vanilla client
# and server controllers), it is needed to provide custom decorator that handles
# additional controllers for new reticles.
###########################################################

# gun_marker_ctrl
@overrideIn(gun_marker_ctrl)
def createGunMarker(func, isStrategic):
    factory = _GunMarkersDPFactory()

    clientFocusReticle = ReticleRegistry.CLIENT_FOCUS
    serverFocusReticle = ReticleRegistry.SERVER_FOCUS
    clientLatencyReticle = ReticleRegistry.CLIENT_LATENCY

    if isStrategic:
        clientMarker = NewSPGGunMarkerController(_MARKER_TYPE.CLIENT, factory.getClientSPGProvider(),
                                                 isMainReticle=True)
        serverMarker = NewSPGGunMarkerController(_MARKER_TYPE.SERVER, factory.getServerSPGProvider(),
                                                 isMainReticle=True)

        clientMarkerFocus = FocusSPGGunMarkerController(clientFocusReticle.gunMarkerType,
                                                        clientFocusReticle.getSpgDataProvider())
        serverMarkerFocus = FocusSPGGunMarkerController(serverFocusReticle.gunMarkerType,
                                                        serverFocusReticle.getSpgDataProvider())

        clientMarkerLatency = NewSPGGunMarkerController(clientLatencyReticle.gunMarkerType,
                                                        clientLatencyReticle.getSpgDataProvider(),
                                                        isMainReticle=False)
    else:
        clientMarker = NewDefaultGunMarkerController(_MARKER_TYPE.CLIENT, factory.getClientProvider(),
                                                     isMainReticle=True)
        serverMarker = NewDefaultGunMarkerController(_MARKER_TYPE.SERVER, factory.getServerProvider(),
                                                     isMainReticle=True)

        clientMarkerFocus = FocusGunMarkerController(clientFocusReticle.gunMarkerType,
                                                     clientFocusReticle.getStandardDataProvider())
        serverMarkerFocus = FocusGunMarkerController(serverFocusReticle.gunMarkerType,
                                                     serverFocusReticle.getStandardDataProvider())

        clientMarkerLatency = NewDefaultGunMarkerController(clientLatencyReticle.gunMarkerType,
                                                            clientLatencyReticle.getStandardDataProvider(),
                                                            isMainReticle=False)

    return NewGunMarkersDecorator(clientMarker, serverMarker, clientMarkerFocus, serverMarkerFocus, clientMarkerLatency)


@overrideIn(gun_marker_ctrl)
def useClientGunMarker(func):
    if g_config.isServerReticleEnabled() or g_config.isLatencyReticleEnabled():
        return True
    return func()


@overrideIn(gun_marker_ctrl)
def useDefaultGunMarkers(func):
    if g_config.isServerReticleEnabled() or g_config.isLatencyReticleEnabled():
        return False
    return func()
