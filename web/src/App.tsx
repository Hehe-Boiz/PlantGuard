import React, { type JSX } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Progress } from "@/components/ui/progress";
import { WiDaySunny } from "react-icons/wi";
import { FaWind } from "react-icons/fa";
import { MdOpacity, MdThermostat, MdWaterDrop } from "react-icons/md";
import { IoMdLeaf } from "react-icons/io";
import { useState, useEffect } from "react";
import { io, Socket } from 'socket.io-client';

interface SensorData {
  temperature: number;
  humidity: number;
  wind: number;
  soilMoisture: number;
  pH: number;
}

interface InfoBoxProps {
  icon: React.ReactNode;
  label: string;
  value: string;
}

export default function Dashboard(): JSX.Element {
  const [data, setData] = useState<SensorData|null>(null);

  useEffect(() => {
    // mặc định path là /socket.io, nhưng do ta dùng adapter path '/ws'
    const socket: Socket = io('http://localhost:8000', {
      path: '/ws',
      transports: ['websocket'], // ép chỉ dùng websocket
    });

    socket.on('connect', () => {
      console.log('Connected with id', socket.id);
    });

    socket.on('sensorData', (msg: SensorData) => {
      setData(msg);
    });

    return () => {
      socket.disconnect();
    };
  }, []);
  return (
    <div className="p-4 space-y-4">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <p className="text-sm text-gray-500">Weilburg, Germany</p>
          <p className="text-lg font-bold">Tue, 10 September 2024</p>
        </div>
        <div className="flex items-center space-x-2">
          <WiDaySunny className="text-3xl text-yellow-400" />
          <span className="text-2xl font-bold">24°C</span>
        </div>
      </div>

      {/* Plant Info */}
      <Card>
        <CardContent className="grid grid-cols-3 gap-4 p-4">
          <div className="col-span-3 flex items-center space-x-2">
            <IoMdLeaf className="text-green-500 text-2xl" />
            <span className="font-bold text-lg">Plant Health</span>
            <span className="text-green-500">DashBoard</span>
          </div>
          <InfoBox icon={<FaWind />} label="Wind" value={`${data?.wind}m/s`} />
          <InfoBox icon={<MdThermostat />} label="Temp" value={`${data?.temperature}`}/>
          <InfoBox icon={<MdOpacity />} label="Humidity" value={`${data?.humidity}%`} />
          <InfoBox icon={<MdWaterDrop />} label="Soil Moisture" value={`${data?.soilMoisture}%`} />
          <InfoBox icon={<span className="text-purple-500">pH</span>} label="pH Level" value={`${data?.pH}`} />
        </CardContent>
      </Card>

      {/* Tasks and Camera */}
      <Card>
        <CardContent className="p-4 space-y-4">
          <div className="font-bold">Task (2/5 Completed)</div>
          <Progress value={40} />
          <ul className="list-disc pl-5 text-sm">
            <li>Water plants with 1 inch of water in the morning</li>
            <li>Apply compost fertilizer</li>
          </ul>
        </CardContent>
      </Card>

      {/* Zone Map */}
      <Card>
        <CardContent className="p-4 space-y-2">
          <div className="font-bold mb-2">Zone Map</div>
          <img src="/greenhouse-map.png" alt="Zone Map" className="rounded-xl" />
          <div className="text-sm text-gray-500">Tap on a section for details</div>
        </CardContent>
      </Card>

      {/* Bottom Tabs */}
      <Tabs defaultValue="plant" className="fixed bottom-0 left-0 right-0 bg-white border-t shadow-md">
        <TabsList className="w-full grid grid-cols-4">
          <TabsTrigger value="plant">Plant</TabsTrigger>
          <TabsTrigger value="alerts">Alerts</TabsTrigger>
          <TabsTrigger value="devices">Devices</TabsTrigger>
          <TabsTrigger value="logs">Logs</TabsTrigger>
        </TabsList>
        <TabsContent value="alerts" className="p-4">Zone 5 dry, Section 3: Leaf disease suspected</TabsContent>
        <TabsContent value="devices" className="p-4">Sensor 04 - Moisture: 65%</TabsContent>
        <TabsContent value="logs" className="p-4">Last watered: 07:30 AM</TabsContent>
      </Tabs>
    </div>
  );
}

function InfoBox({ icon, label, value }: InfoBoxProps): JSX.Element {
  return (
    <div className="bg-gray-100 rounded-xl p-3 flex flex-col items-center">
      <div className="text-xl mb-1">{icon}</div>
      <p className="text-xs text-gray-500">{label}</p>
      <p className="text-base font-semibold">{value}</p>
    </div>
  );
}
