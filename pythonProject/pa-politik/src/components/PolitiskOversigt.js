import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const PolitiskOversigt = () => {
  // Gem aktivt tab i localStorage
  const [activeTab, setActiveTab] = useState(() => {
    return localStorage.getItem('activeTab') || 'konkrete';
  });

  useEffect(() => {
    localStorage.setItem('activeTab', activeTab);
  }, [activeTab]);

  const konkreteSager = [
    "Batterier i landzoner",
    "Beredskabsaftale",
    "Biomasse",
    "Brintrør",
    "Cybersikkerhed",
    "Elforsyningsloven",
    "Energiø Bornholm (EØB)",
    "Esbjergruten",
    "Forsvar (VE-areal)",
    "Forsvarsforlig",
    "Frivillig brancheaftale om erstatningsnatur (med Green Power Denmark, DN og DI)",
    "Grøn Luftfart",
    "Havvind - særligt rammevilkår efter 2030",
    "Investeringscreeningsloven (Overvåges)",
    "Konkret lovforslag (første halvdel af næste år)",
    "NEKST for Elnet (VVM-screening, ekspropriering)",
    "NIS 2 og CER-direktivet (Kommende sager)",
    "Realkredit",
    "Testcenter",
    "Udbudskriterier i EU (Kommende sag)"
  ];

  const strategiskePrioriteringer = [
    "A-projekt (aktiv deltagelse)",
    "COP og UNGA",
    "EU-formandskab",
    "EU grid fokus",
    "Energinet tariffer og gebyrer",
    "FL26",
    "Folkemøde 2026",
    "Grøn trepart",
    "Kommunalvalg",
    "Klimamålsætninger / Evaluering af klimalov",
    "Ny EU-Kommission og EP (relationsopbygning mv.)",
    "Statusmøder med ministerier",
    "VE-land (+ konference)"
  ];

  const samarbejdsorganer = [
    "Cybersikkerhedsalliancen",
    "Grønt Erhvervsforum",
    "Parnerskabet for Havvind",
    "VE-alliancen (land)",
    "\"Syv Styrker\""
  ];

  const tabData = {
    konkrete: {
      title: "Konkrete sager",
      items: konkreteSager,
      color: "from-blue-500 to-blue-600"
    },
    strategiske: {
      title: "Strategiske prioriteringer",
      items: strategiskePrioriteringer,
      color: "from-green-500 to-green-600"
    },
    samarbejde: {
      title: "Samarbejdsorganer",
      items: samarbejdsorganer,
      color: "from-purple-500 to-purple-600"
    }
  };

  const containerVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.5,
        staggerChildren: 0.1
      }
    },
    exit: {
      opacity: 0,
      y: -20,
      transition: {
        duration: 0.3
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, x: -20, scale: 0.95 },
    visible: {
      opacity: 1,
      x: 0,
      scale: 1,
      transition: {
        type: "spring",
        stiffness: 100,
        damping: 10,
        duration: 0.5
      }
    },
    hover: {
      scale: 1.02,
      boxShadow: "0 10px 20px rgba(0,0,0,0.1)",
      transition: {
        duration: 0.2
      }
    }
  };

  const TabButton = ({ id, title }) => (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={() => setActiveTab(id)}
      className={`px-6 py-3 rounded-lg transition-all duration-300 transform
        ${activeTab === id 
          ? `bg-gradient-to-r ${tabData[id].color} text-white shadow-lg scale-105`
          : 'bg-white text-gray-600 hover:bg-gray-50 border border-gray-200'
        }
        font-semibold focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500`}
    >
      {title}
    </motion.button>
  );

  const CardContent = ({ item, index }) => (
    <motion.div
      variants={itemVariants}
      initial="hidden"
      animate="visible"
      whileHover="hover"
      custom={index}
      className={`bg-white p-6 rounded-xl shadow-sm hover:shadow-xl 
        transition-all duration-300 border border-gray-100
        transform hover:-translate-y-1`}
    >
      <div className="flex items-start space-x-3">
        <div className="flex-shrink-0">
          <div className={`w-2 h-2 rounded-full mt-2 bg-gradient-to-r ${tabData[activeTab].color}`} />
        </div>
        <p className="text-gray-700 font-medium">{item}</p>
      </div>
    </motion.div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 p-4 md:p-8">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-7xl mx-auto bg-white rounded-3xl shadow-xl"
      >
        <div className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-t-3xl p-8 md:p-12">
          <motion.h1
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-3xl md:text-4xl font-bold text-white mb-4"
          >
            UDSKAST: PA – politiske sager
          </motion.h1>

          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-blue-100 text-lg"
          >
            Denne oversigt præsenterer de vigtigste politiske sager,
            som PA arbejder med eller følger.
          </motion.p>
        </div>

        <div className="p-8">
          <div className="flex flex-wrap gap-4 mb-8">
            {Object.entries(tabData).map(([id, { title }]) => (
              <TabButton key={id} id={id} title={title} />
            ))}
          </div>

          <AnimatePresence mode="wait">
            <motion.div
              key={activeTab}
              variants={containerVariants}
              initial="hidden"
              animate="visible"
              exit="exit"
              className="bg-gray-50 rounded-2xl p-6 md:p-8"
            >
              <motion.div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {tabData[activeTab].items.map((item, index) => (
                  <CardContent key={item} item={item} index={index} />
                ))}
              </motion.div>
            </motion.div>
          </AnimatePresence>
        </div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="bg-gradient-to-r from-gray-50 to-blue-50 rounded-b-3xl p-6 text-right"
        >
          <p className="text-sm text-gray-500 italic">
            Opdateret 11/11 2024
          </p>
        </motion.div>
      </motion.div>
    </div>
  );
};

export default PolitiskOversigt;