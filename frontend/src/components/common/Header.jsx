import { Leaf, Coins, Flame, LogOut, Trophy, ShoppingBag, Target, Camera, Globe, Info, Mail, Menu } from 'lucide-react';
import { Link, useNavigate, useLocation } from 'react-router-dom';

// ... (context imports remain)

// ... (component start)

return (
    <>
        <header className="sticky top-0 z-50 w-full bg-white/90 backdrop-blur-md border-b border-slate-100 shadow-sm">
            <div className="max-w-7xl mx-auto px-4 h-16 flex justify-between items-center gap-4">

                {/* LEFT: Brand & Main Nav */}
                <div className="flex items-center gap-8">
                    <Link to={isLoggedIn ? "/dashboard" : "/"} className="flex items-center gap-2 group">
                        <div className="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center text-white shadow-green-200 shadow-md group-hover:rotate-6 transition-transform">
                            <Leaf className="w-5 h-5" />
                        </div>
                        <span className="font-black text-xl text-slate-800 tracking-tight hidden sm:block">EcoLoop</span>
                    </Link>

                    {isLoggedIn && (
                        <nav className="hidden md:flex items-center gap-1">
                            <NavLink to="/dashboard" label="Play" />
                            <NavLink to="/community" label="Community" />
                            <NavLink to="/about" label="About" />
                            <NavLink to="/contact" label="Contact" />
                        </nav>
                    )}
                </div>

                {/* RIGHT: Stats & Actions */}
                <div className="flex items-center gap-3">
                    {!isLoggedIn ? (
                        <div className="flex gap-4 items-center">
                            <Link to="/about" className="text-sm font-bold text-slate-500 hover:text-green-600">About</Link>
                            <Link to="/contact" className="text-sm font-bold text-slate-500 hover:text-green-600">Contact</Link>
                            <Link to="/" className="bg-green-600 text-white px-5 py-2 rounded-full font-bold text-sm hover:bg-green-700 transition shadow-lg shadow-green-200">
                                Login
                            </Link>
                        </div>
                    ) : (
                        <>
                            {/* Stats Group (n1 style) */}
                            <div className="hidden lg:flex items-center gap-3 bg-slate-50 px-3 py-1.5 rounded-xl border border-slate-100 mr-2">
                                <div
                                    className="flex items-center gap-1.5 cursor-pointer hover:opacity-80 transition"
                                    onClick={() => setShowCalendar(true)}
                                    title="View Streak"
                                >
                                    <Flame className="w-4 h-4 text-orange-500 fill-orange-500 animate-pulse" />
                                    <span className="font-extrabold text-slate-700 text-sm">{user.streak}</span>
                                </div>
                                <div className="w-px h-4 bg-slate-200"></div>
                                <div className="flex items-center gap-1.5">
                                    <Coins className="w-4 h-4 text-yellow-500 fill-yellow-400" />
                                    <span className="font-extrabold text-slate-700 text-sm">{user.coins}</span>
                                </div>
                            </div>

                            {/* Tools Group (Icons) */}
                            <div className="flex items-center gap-2">
                                {/* Scanner Trigger (n2 feature) */}
                                <button
                                    onClick={() => setIsScannerOpen(true)}
                                    className="p-2 bg-blue-50 text-blue-600 rounded-full hover:bg-blue-100 transition shadow-sm relative group w-10 h-10 flex items-center justify-center"
                                    title="AI Eco-Scanner"
                                >
                                    <Camera className="w-5 h-5" />
                                    <div className="absolute -top-1 -right-1 w-3 h-3 bg-blue-500 rounded-full border-2 border-white animate-pulse shadow-sm"></div>
                                </button>

                                {/* Challenges (n1) */}
                                <button
                                    onClick={() => setIsChallengesOpen(true)}
                                    className="relative w-10 h-10 flex items-center justify-center rounded-xl bg-slate-50 text-slate-500 hover:bg-white hover:text-emerald-600 hover:shadow-md transition-all group"
                                    title="Challenges"
                                >
                                    <div className="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full border border-white z-10"></div>
                                    <Target className="w-5 h-5" strokeWidth={2.5} />
                                </button>

                                <IconButton to="/leaderboard" icon={Trophy} title="Leaderboard" />
                                <IconButton to="/store" icon={ShoppingBag} title="Store" />

                                {/* Divider */}
                                <div className="w-px h-8 bg-slate-100 mx-1"></div>

                                {/* Profile */}
                                <Link to="/profile" className="flex items-center gap-2 group">
                                    <div className="w-9 h-9 bg-green-100 rounded-full flex items-center justify-center border-2 border-green-500 group-hover:border-green-600 transition overflow-hidden shadow-sm" title={user.username}>
                                        <span className="text-lg">👩‍🎓</span>
                                    </div>
                                </Link>

                                <button onClick={handleLogout} className="text-slate-300 hover:text-red-500 transition ml-1" title="Logout">
                                    <LogOut className="w-5 h-5" />
                                </button>
                            </div>
                        </>
                    )}
                </div>
            </div>

            {/* Modals outside the flex container but inside header component or fragment */}
            <ScannerModal
                isOpen={isScannerOpen}
                onClose={() => setIsScannerOpen(false)}
            />
        </header>
    </div >

        {/* Tools Group (Icons) */ }
        < div className = "flex items-center gap-2" >
                                    <button
                                        onClick={() => setIsChallengesOpen(true)}
                                        className="relative w-10 h-10 flex items-center justify-center rounded-xl bg-slate-50 text-slate-500 hover:bg-white hover:text-emerald-600 hover:shadow-md transition-all group"
                                        title="Challenges"
                                    >
                                        <div className="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full border border-white z-10"></div>
                                        <Target className="w-5 h-5" strokeWidth={2.5} />
                                    </button>

                                    <IconButton to="/leaderboard" icon={Trophy} title="Leaderboard" />
                                    <IconButton to="/store" icon={ShoppingBag} title="Store" />

{/* Divider */ }
<div className="w-px h-8 bg-slate-100 mx-1"></div>

{/* Profile */ }
                                    <Link to="/profile" className="flex items-center gap-2 group">
                                        <div className="w-9 h-9 bg-slate-100 rounded-full flex items-center justify-center border-2 border-transparent group-hover:border-green-200 transition overflow-hidden">
                                            <span className="text-lg">👩‍🎓</span>
                                        </div>
                                    </Link>

                                    <button onClick={handleLogout} className="text-slate-300 hover:text-red-500 transition ml-1" title="Logout">
                                        <LogOut className="w-5 h-5" />
                                    </button>
                                </div >
                            </>
                        )}
                    </div >
                </div >
            </header >


    {/* Streak Calendar Modal */ }
{
    isLoggedIn && (
        <>
            <StreakCalendar
                isOpen={showCalendar}
                onClose={() => setShowCalendar(false)}
                streak={user.streak}
            />
            <ChallengesModal
                isOpen={isChallengesOpen}
                onClose={() => setIsChallengesOpen(false)}
            />
        </>
    )
}
        </>
    );
};

export default Header;
