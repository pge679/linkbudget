__author__ = 'thanatv'

from django.contrib import admin
from mysite.models import Progress
from linkbudget.models import *


class ProgressAdmin(admin.ModelAdmin):
    pass


# ------------------- Tabular Inline Class -------------------------------

class UplinkDefinedContourInline(admin.TabularInline):
    model = UplinkDefinedContour


class DownlinkDefinedContourInline(admin.TabularInline):
    model = DownlinkDefinedContour


class AlcFullLoadBackoffInline(admin.TabularInline):
    model = AlcFullLoadBackoff


class TransponderCharacteristicInline(admin.TabularInline):
    model = TransponderCharacteristic


class AntennaGainInline(admin.TabularInline):
    model = AntennaGain


class AntennaGTInline(admin.TabularInline):
    model = AntennaGT


class AntennaNoiseTemperatureInline(admin.TabularInline):
    model = AntennaNoiseTemperature


class TransmitBandInline(admin.TabularInline):
    model = TransmitBand
    extra = 1


class ReceiveBandInline(admin.TabularInline):
    model = ReceiveBand
    extra = 1


class AvailableSymbolRateInline(admin.TabularInline):
    model = AvailableSymbolRate


class MCGInline(admin.TabularInline):
    model = MCG


class ModemOperationModeInline(admin.TabularInline):
    model = ModemOperationMode
    extra = 1

# ------------------- Admin Class --------------------------------------

class FrequencyBandAdmin(admin.ModelAdmin):
    pass


class SatelliteAdmin(admin.ModelAdmin):
    pass


class UplinkBeamAdmin(admin.ModelAdmin):
    inlines = [
        UplinkDefinedContourInline,
    ]


class DownlinkBeamAdmin(admin.ModelAdmin):
    inlines = [
        DownlinkDefinedContourInline,
    ]


class TransponderAdmin(admin.ModelAdmin):
    inlines = [
        AlcFullLoadBackoffInline,
        TransponderCharacteristicInline,
    ]


class ChannelAdmin(admin.ModelAdmin):
    pass


class AntennaVendorAdmin(admin.ModelAdmin):
    pass


class AntennaAdmin(admin.ModelAdmin):
    inlines = [
        AntennaGainInline,
        AntennaGTInline,
        AntennaNoiseTemperatureInline,
        TransmitBandInline,
        ReceiveBandInline,
    ]


class LocationAdmin(admin.ModelAdmin):
    pass


class GatewayAdmin(admin.ModelAdmin):
    pass


class HpaAdmin(admin.ModelAdmin):
    pass


class StationAdmin(admin.ModelAdmin):
    pass


class ModemVendorAdmin(admin.ModelAdmin):
    pass


class ModemAdmin(admin.ModelAdmin):
    inlines = [
        ModemOperationModeInline
    ]


class ModemApplicationAdmin(admin.ModelAdmin):
    inlines = [
        AvailableSymbolRateInline,
        MCGInline,
    ]



# Register project progress model
admin.site.register(Progress, ProgressAdmin)

# Register linkbudget model
admin.site.register(FrequencyBand, FrequencyBandAdmin)
admin.site.register(Satellite, SatelliteAdmin)
admin.site.register(UplinkBeam, UplinkBeamAdmin)
admin.site.register(DownlinkBeam, DownlinkBeamAdmin)
admin.site.register(Transponder, TransponderAdmin)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(AntennaVendor, AntennaVendorAdmin)
admin.site.register(Antenna, AntennaAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Gateway, GatewayAdmin)
admin.site.register(Hpa, HpaAdmin)
admin.site.register(Station, StationAdmin)
admin.site.register(ModemVendor, ModemVendorAdmin)
admin.site.register(Modem, ModemAdmin)
admin.site.register(ModemApplication, ModemApplicationAdmin)

