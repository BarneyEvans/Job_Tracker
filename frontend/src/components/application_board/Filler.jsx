export default function Filler({stageName}) {

return (
    <div className="flex-1 bg-[#EDF6F9] p-4 border-r border-b border-[#b7c2c5b0] flex flex-col min-h-screen">
            <h2 className="font-bold mb-4 p-1 text-center">{stageName}</h2>
            <div className="flex-1">
            {/* Placeholder */}
            <div className="flex-1 bg-white p-4 rounded-lg border border-[#b7c2c5b0] min-h-[200px]">
                <div className="h-6 w-1/2 bg-gray-200 rounded mb-4"></div>
                <div className="h-4 w-full bg-gray-200 rounded mb-2"></div>
                <div className="h-4 w-3/4 bg-gray-200 rounded mb-2"></div>
            </div>
            </div>
    </div>
      );}