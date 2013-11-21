__author__ = 'thanatv'

# Main class for link calculation.
from linkbudget.models import *
from scipy.interpolate import interp1d

# Link budget constants
BOLTZMANN_CONSTANT = -228.6  # dBJ/K
SPEED_OF_LIGHT = 300000000  # m/s
EQUATORIAL_EARTH_RADIUS = 6378.14  # km
EARTH_FLATTENING_FACTOR = 0.003352813
GEOSYNCHRONOUS_ALTITUDE = 35786  # km


class LinkCalcError(Exception):
    pass


class Link:
    def __init__(self, channel, modem, bandwidth, uplink_station=None,
                 downlink_station=None, gateway=None, rain_model=None, power_optimization=True,
                 power_overused=0, num_carriers_in_transponder=10, force_operating_mode=None):
        """
        Initialize the parameters required for the link budget.
        Required parameters: channel, modem and bandwidth
        Optional parameters: uplink station, downlink station, rain model, power optimization, overused power,
        number of carriers in the transponders
        """
        self.channel = channel
        self.modem = modem
        self.bandwidth = bandwidth
        self.uplink_station = uplink_station
        self.downlink_station = downlink_station
        self.gateway = gateway
        self.rain_model = rain_model
        self.power_optimization = power_optimization
        self.power_overused = power_overused
        self.num_carriers_in_transponder = num_carriers_in_transponder
        self.force_operating_mode = force_operating_mode
        self.result = LinkResult()


    def calculate(self):
        """
        Calculate a link budget and return a result object
        """
        uplink = self.result.uplink
        downlink = self.result.downlink

        # Seek the optimized uplink power. This is the default case unless
        # is_power_optimized is explicitly assigned false.
        # Ex. the IPSTAR return channel normally calculates with full BUC power
        # so no power optimization required.
        uplink.gt = self.channel.uplink_beam.peak_gt  # Beam peak
        #self.seek_optimized_eirp_uplink(self.channel.transponder, uplink.gt)

        # ---- C/N Uplink ----

        # For forward or broadcast channel, check whether the uplink station is specified.
        # If not, use the default gateway of the channel
        # If uplink station is specified, check the following for usage compatibility:
        # 1. Antenna's transmit frequency range and polarization matches the beam
        # 2. Uplink location is in the beam coverage
        # Return error if requirements are not met
        if self.uplink_station and isinstance(self.uplink_station, Station):
            pass

        # Compute C/N Uplink (clear sky and rain fade)

        # ---- C/N Downlink ----

        # Compute EIRP downlink of the channel from uplink power flux density and satellite settings

        # For return channel, check whether the downlink station is specified.
        # If not, use the default gateway of the channel
        # If downlink station is specified, check the following for usage compatibility:
        # 1. Antenna's receive frequency range and polarization matches the beam
        # 2. Downlink location is in the beam coverage
        # Return error if requirements are not met

        # Compute C/N Downlink (clear sky, up fade only, down fade only and both fade from default availability)

        # ---- C/I ----

        # Compute the value of C/I from power source if it has default value of C/I3IM or NPR in the database.

        # Compute C/I from satellite if it has default value of transponder's C/I3M or NPR

        # Compute C/I uplink from adjacent satellites

        # Compute C/I downlink from adjacent satellites

        # Compute C/I uplink from adjacent cells

        # Compute C/I downlink from adjacent cells

        # ---- C/N Total ----

        # Compute C/N Total (clear sky, up fade only, down fade only and both fade )

        # ---- Capacity ----
        # Compute link capacity (clear sky, up fade only, down fade only and both fade )
        # in both MHz and Mbps

        # Pick the MCG at both fade and calculate capacity. If the modem has no ACM function, let capacity
        # at clear sky equals to capacity at both fade

        # Else, pick MCG at clear sky and calculate capacity separately for clear sky condition.

        # Seek the maximum total link availability if needed.

        # Record all parameters into the result object

        return self.result

    def seek_optimized_eirp_uplink(self, transponder, bandwidth, gt_at_location, forced_operating_mode=None,
                                   required_output_backoff=0, fca_step=0):
        """
        Seek an optimized EIRP uplink of the uplink station
        """

        # If the operating mode is not forced by user (which should be a normal case), use the transponder's primary
        # mode
        operating_mode = ""
        if forced_operating_mode:
            operating_mode = forced_operating_mode
        else:
            operating_mode = transponder.primary_mode

        #try:
        #    self.validate_transponder_mode(transponder, operating_mode)
        #except LinkCalcError, err:
        #    print err.message
        #finally:
        #    pass

        # In FGM mode, maximum allowable EIRP is equal to an amount that drives the amplifier to get required OBO
        # Default OBO = 0 dB
        if operating_mode is "FGM":
        # TODO Add calculation for different FCA steps



        # Log an error if the transponder doesn't have the given operating mode

            def validate_transponder_mode(self, transponder, operating_mode):
                if not operating_mode in (transponder.primary_mode, transponder.secondary_mode):
                    #raise LinkCalcError("Transponder {0} doesn't have {1} mode.".format(transponder.name, operating_mode))
                    self.log_error("Transponder {0} doesn't have {1} mode.".format(transponder.name, operating_mode))


        def log_error(self, message):
            self.result.error_messages.append(message)


class LinkResult(object):
    def __init__(self):
        self.uplink = UplinkResult()
        self.satellite = SatelliteResult()
        self.downlink = DownlinkResult()
        self.uplink_interferences = UplinkInterferencesResult()
        self.downlink_interferences = DownlinkInterferencesResult()
        self.clear_sky = ClearSkyResult()
        self.rain_up = RainUplinkResult()
        self.rain_down = RainDownlinkResult()
        self.rain_both = RainBothResult()
        self.warning_messages = []
        self.error_messages = []

    def display(self):
        print "-------------"
        print "Uplink"
        print "EIRP: {0} dBW".format(self.uplink.eirp)
        print "G/T {0} dB/K".format(self.uplink.gt)
        print "Path Loss {0} dB".format(self.uplink.path_loss)
        print "Noise BW {0} dB".format(self.uplink.noise_bw)
        print "C/N Uplink {0} dB".format(self.uplink.cn)
        print "-------------"
        print "downlink"
        print "EIRP: {0} dBW".format(self.downlink.eirp)
        print "G/T {0} dB/K".format(self.downlink.gt)
        print "Path Loss {0} dB".format(self.downlink.path_loss)
        print "Noise BW {0} dB".format(self.downlink.noise_bw)
        print "C/N downlink {0} dB".format(self.downlink.cn)
        print "--------------"
        print "C/N Total {0} dB".format(self.cn_total)


class UplinkResult(object):
    def __init__(self):
        self.latitude = 0
        self.longitude = 0
        self.polarization = ""
        self.slant_range = 0
        self.frequency = 0
        self.elevation = 0
        self.antenna_diameter = 0
        self.antenna_efficiency = 0
        self.antenna_gain = 0
        self.hpa_output_power = 0
        self.spreading_loss = 0
        self.relative_contour = 0
        self.gt = 0
        self.optimized_eirp = 0
        self.eirp = 0
        self.upc = 0
        self.pfd = 0
        self.availability = 0
        self.pointing_loss = 0
        self.xpol_loss = 0
        self.axial_ratio_loss = 0
        self.path_loss = 0
        self.cloud_attenuation = 0
        self.gas_attenuation = 0
        self.scin_attenuation = 0
        self.rain_attenuation = 0


class SatelliteResult(object):
    def __init__(self):
        self.name = ""
        self.orbital_slot = 0
        self.half_station_keeping_box = 0
        self.channel_bandwidth = 0
        self.peak_gt = 0
        self.channel_sfd = 0
        self.channel_input_backoff = 0
        self.channel_output_backoff = 0
        self.carrier_output_backoff = 0
        self.peak_saturated_eirp = 0
        self.gain_variation = 0


class DownlinkResult(object):
    def __init__(self):
        self.latitude = 0
        self.longitude = 0
        self.polarization = ""
        self.slant_range = 0
        self.frequency = 0
        self.azimuth = 0
        self.elevation = 0
        self.antenna_diameter = 0
        self.antenna_efficiency = 0
        self.antenna_gain = 0
        self.ifl_loss = 0
        self.lnb_gain = 0
        self.lnb_temp = 0
        self.clearsky_noise_temp = 0
        self.clearsky_gt = 0
        self.rain_noise_temp = 0
        self.rain_gt = 0
        self.availability = 0
        self.pointing_loss = 0
        self.xpol_loss = 0
        self.axial_ratio_loss = 0
        self.path_loss = 0
        self.cloud_attenuation = 0
        self.gas_attenuation = 0
        self.scin_attenuation = 0
        self.rain_attenuation = 0


class UplinkInterferencesResult(object):
    def __init__(self):
        self.adjacent_cells = 50
        self.adjacent_satellite = 50
        self.intermodulation = 50


class DownlinkInterferencesResult(object):
    def __init__(self):
        self.adjacent_cells = 50
        self.adjacent_cells = 50
        self.intermodulation = 50


class ClearSkyResult(object):
    def __init__(self):
        self.cn_uplink = 0
        self.cn_downlink = 0
        self.ci_uplink = 0
        self.ci_downlink = 0
        self.cn_total = 0


class RainUplinkResult(object):
    def __init__(self):
        self.cn_uplink = 0
        self.cn_downlink = 0
        self.ci_uplink = 0
        self.ci_downlink = 0
        self.cn_total = 0


class RainDownlinkResult(object):
    def __init__(self):
        self.cn_uplink = 0
        self.cn_downlink = 0
        self.ci_uplink = 0
        self.ci_downlink = 0
        self.cn_total = 0


class RainBothResult(object):
    def __init__(self):
        self.cn_uplink = 0
        self.cn_downlink = 0
        self.ci_uplink = 0
        self.ci_downlink = 0
        self.cn_total = 0