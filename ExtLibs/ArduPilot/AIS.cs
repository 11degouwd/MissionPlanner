using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Text;
using log4net;

namespace MissionPlanner.ArduPilot
{
    public class AIS
    {
        private static readonly ILog log = LogManager.GetLogger(MethodBase.GetCurrentMethod().DeclaringType);

        static List<MAVLink.mavlink_ais_vessel_t> _Vessels = new List<MAVLink.mavlink_ais_vessel_t>();

        public static MAVLink.mavlink_ais_vessel_t[] Vessels
        {
            get { return _Vessels.ToArray(); }
        }

        public static void Start(MAVLinkInterface mav)
        {
            mav.OnPacketReceived += (sender, message) =>
            {
                if (message.msgid == (uint) MAVLink.MAVLINK_MSG_ID.AIS_VESSEL)
                {
                    try
                    {
                        var msg = (MAVLink.mavlink_ais_vessel_t) message.data;

                        lock (_Vessels)
                        {
                            var existing = Vessels.Where(a => a.MMSI == msg.MMSI);
                            if (existing.Count() == 0)
                            {
                                _Vessels.Add(msg);
                            }
                            else
                            {
                                _Vessels.Remove(existing.First());
                                _Vessels.Add(msg);
                            }
                        }
                    }
                    catch (Exception ex)
                    {
                        log.Error(ex);
                    }
                }
            };
        }
    }
}