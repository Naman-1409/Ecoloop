import React from 'react';
import Header from '../components/common/Header';
import GameMap from '../components/map/GameMap';
import { motion } from 'framer-motion';
import { Compass } from 'lucide-react';

const Dashboard = () => {
    return (
        <div className="min-h-screen bg-green-50 pb-20 overflow-x-hidden selection:bg-green-200">
            <Header />
            
            <main className="w-full px-4 flex flex-col items-center">
                <motion.div 
                    initial={{ y: -20, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    className="text-center mb-10 mt-4"
                >
                    <div className="flex items-center justify-center gap-2 mb-2">
                        <Compass className="text-green-600 animate-spin-slow" size={24} />
                        <h1 className="text-5xl font-black text-green-900 tracking-tight">World Explorer</h1>
                    </div>
                    <p className="text-green-700 font-bold text-lg bg-green-100/50 px-6 py-2 rounded-full inline-block">
                        Complete challenges to heal the environment! 🌱
                    </p>
                </motion.div>

                <div className="w-full h-full flex-1 relative">
                    {/* Decorative elements */}
                    <div className="absolute top-0 left-0 w-64 h-64 bg-green-200/30 rounded-full blur-3xl -z-10 animate-pulse"></div>
                    <div className="absolute bottom-0 right-0 w-96 h-96 bg-blue-100/30 rounded-full blur-3xl -z-10"></div>
                    
                    <GameMap />
                </div>
            </main>
        </div>
    );
};

export default Dashboard;
