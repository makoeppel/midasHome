"""
Ruuvi midas frontend to readout multiple ruuvi sensors
"""

import midas
import midas.frontend
import midas.event

from ruuvitag_sensor.ruuvi import RuuviTagSensor


class RuuviEquipment(midas.frontend.EquipmentBase):
    def __init__(self, client):
        # The name of our equipment. This name will be used on the midas status
        # page, and our info will appear in /Equipment/RuuviEquipment in
        # the ODB.
        equip_name = "Ruuviquipment"

        # Define the "common" settings of a frontend. These will appear in
        # /Equipment/RuuviEquipment/Common. The values you set here are
        # only used the very first time this frontend/equipment runs; after 
        # that the ODB settings are used.
        default_common = midas.frontend.InitialEquipmentCommon()
        default_common.equip_type = midas.EQ_PERIODIC
        default_common.buffer_name = "SYSTEM"
        default_common.trigger_mask = 0
        default_common.event_id = 1
        default_common.period_ms = 100
        default_common.read_when = midas.RO_RUNNING | midas.RO_STOPPED
        default_common.log_history = 1

        # setup the ODB
        settings = {"NAME": ["EG", "OG", "Bad"],
                    "MAC": ["E5:C5:29:91:A2:5E", "ED:91:8B:2F:BF:D6", "EC:DC:87:B8:02:D0"],
                    "timeout": 4,
                    "batteryNorm": 3100,
                    "Names RUBK": [
                        "TempEG", "HumidityEG", "BatteryEG",
                        "TempOG", "HumidityOG", "BatteryOG",
                        "TempBad", "HumidityBad", "BatteryBad",
                    ]
        }

        # You MUST call midas.frontend.EquipmentBase.__init__ in your equipment's __init__ method!
        midas.frontend.EquipmentBase.__init__(
                self, client, equip_name, default_common, settings
        )

        # You can set the status of the equipment (appears in the midas status page)
        self.set_status("Initialized")
        
    def readout_func(self):
        """
        For a periodic equipment, this function will be called periodically
        (every 100ms in this case). It should return either a `midas.event.Event`
        or None (if we shouldn't write an event).
        """

        # In this example, we just make a simple event with one bank.
        event = midas.event.Event()

        all_macs = False
        event_data = []
        while not all_macs:
            all_macs = True
            # get sensors data
            data = RuuviTagSensor.get_data_for_sensors(
                self.settings["MAC"],
                self.settings["timeout"]
            )

            # create event
            event_data = []
            for mac in self.settings["MAC"]:
                if mac not in data:
                    all_macs = False
                    break
                event_data.append(data[mac]["temperature"])
                event_data.append(data[mac]["humidity"])
                event_data.append(data[mac]["battery"] / self.settings["batteryNorm"])
        event.create_bank("RUBK", midas.TID_FLOAT, event_data)

        return event

class RuuviFrontend(midas.frontend.FrontendBase):
    """
    A frontend contains a collection of equipment.
    You can access self.client to access the ODB etc (see `midas.client.MidasClient`).
    """
    def __init__(self):
        # You must call __init__ from the base class.
        midas.frontend.FrontendBase.__init__(self, "ruuvife")
        
        # You can add equipment at any time before you call `run()`, but doing
        # it in __init__() seems logical.
        self.add_equipment(RuuviEquipment(self.client))
        
    def begin_of_run(self, run_number):
        """
        This function will be called at the beginning of the run.
        You don't have to define it, but you probably should.
        You can access individual equipment classes through the `self.equipment`
        dict if needed.
        """
        self.set_all_equipment_status("Running", "greenLight")
        self.client.msg("Frontend has seen start of run number %d" % run_number)
        return midas.status_codes["SUCCESS"]
        
    def end_of_run(self, run_number):
        self.set_all_equipment_status("Finished", "greenLight")
        self.client.msg("Frontend has seen end of run number %d" % run_number)
        return midas.status_codes["SUCCESS"]
    
    def frontend_exit(self):
        """
        Most people won't need to define this function, but you can use
        it for final cleanup if needed.
        """
        print("Goodbye from user code!")
        
if __name__ == "__main__":
    # The main executable is very simple - just create the frontend object,
    # and call run() on it.
    with RuuviFrontend() as my_fe:
        my_fe.run()
