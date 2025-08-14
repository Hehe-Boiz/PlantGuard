import React, { type JSX } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Progress } from "@/components/ui/progress";
import { WiDaySunny } from "react-icons/wi";
import { FaWind } from "react-icons/fa";
import { MdOpacity, MdThermostat, MdWaterDrop } from "react-icons/md";
import { IoMdLeaf } from "react-icons/io";
import { useState, useEffect } from "react";
import { Badge } from "@/components/ui/badge";


interface SensorData {
  temperature: number;
  humidity: number;
  wind: number;
  soilMoisture: number;
}

interface InfoBoxProps {
  icon: React.ReactNode;
  label: string;
  value: string;
}

export default function Dashboard(): JSX.Element {
  const [data, setData] = useState<SensorData | null>(null);
  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8000/ws")
    socket.onmessage = (event) => {
      const msg = JSON.parse(event.data)
      setData(msg)
    }
    return () => {
      socket.close()
    }
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
          <InfoBox icon={<MdThermostat />} label="Temp" value={`${data?.temperature}`} />
          <InfoBox icon={<MdOpacity />} label="Humidity" value={`${data?.humidity}%`} />
          <InfoBox icon={<MdWaterDrop />} label="Soil Moisture" value={`${data?.soilMoisture}%`} />
        </CardContent>
      </Card>

      {/* Tasks and Camera */}
      {/* <Card>
        <CardContent className="p-4 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4 items-center rounded-2xl border bg-muted/30 p-4">
            <div className="md:col-span-2">
              <div className="relative w-full aspect-[4/3] overflow-hidden rounded-xl bg-white">
                <img className="w-full h-full object-cover" />
              </div>
            </div>
          </div>
        </CardContent>
      </Card> */}

      {/* Bottom Tabs */}
      {/* <Tabs defaultValue="plant" className="fixed bottom-0 left-0 right-0 bg-white border-t shadow-md">
        <TabsList className="w-full grid grid-cols-4">
          <TabsTrigger value="plant">Plant</TabsTrigger>
          <TabsTrigger value="alerts">Alerts</TabsTrigger>
          <TabsTrigger value="devices">Devices</TabsTrigger>
          <TabsTrigger value="logs">Logs</TabsTrigger>
        </TabsList>
        <TabsContent value="alerts" className="p-4">Zone 5 dry, Section 3: Leaf disease suspected</TabsContent>
        <TabsContent value="devices" className="p-4">Sensor 04 - Moisture: 65%</TabsContent>
        <TabsContent value="logs" className="p-4">Last watered: 07:30 AM</TabsContent>
      </Tabs> */}
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
