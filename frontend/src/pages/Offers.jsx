import OffersNav from "../components/navbar_components/OffersNav";
import Sidebar from "../components/side_bar/Sidebar";

export default function Offers() {
    return (
        <div className="flex h-screen overflow-hidden">
            <Sidebar />
            <div className="flex-1 flex flex-col">
                <OffersNav />
            </div>
        </div>
    )
}
