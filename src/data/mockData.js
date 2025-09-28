// Mock data for FasalNeeti application

// Sample farmer data
export const mockFarmers = [
  {
    id: 1,
    name: "राम कुमार शर्मा",
    location: "पंजाब, लुधियाना",
    mobile: "+91 98765 43210",
    fertilizerUsage: "Organic + NPK",
    soilType: "Alluvial",
    soilPH: 6.8,
    lastCrop: "गेहूं (Wheat)",
    irrigationType: "Drip Irrigation",
    pesticidesUsed: "Neem-based organic",
    registrationDate: "2024-01-15"
  },
  {
    id: 2,
    name: "सुनीता देवी",
    location: "उत्तर प्रदेश, मेरठ",
    mobile: "+91 87654 32109",
    fertilizerUsage: "DAP + Urea",
    soilType: "Clay Loam",
    soilPH: 7.2,
    lastCrop: "धान (Rice)",
    irrigationType: "Flood Irrigation",
    pesticidesUsed: "Minimal chemical",
    registrationDate: "2024-02-20"
  },
  {
    id: 3,
    name: "अजय पटेल",
    location: "गुजरात, अहमदाबाद",
    mobile: "+91 76543 21098",
    fertilizerUsage: "Vermicompost",
    soilType: "Sandy Loam",
    soilPH: 6.5,
    lastCrop: "कपास (Cotton)",
    irrigationType: "Sprinkler",
    pesticidesUsed: "Integrated Pest Management",
    registrationDate: "2024-03-10"
  }
];

// Yield prediction data for charts
export const yieldPredictionData = [
  { month: 'Jan', predicted: 45, actual: 42, optimal: 50 },
  { month: 'Feb', predicted: 52, actual: 48, optimal: 55 },
  { month: 'Mar', predicted: 48, actual: 51, optimal: 52 },
  { month: 'Apr', predicted: 61, actual: 58, optimal: 65 },
  { month: 'May', predicted: 55, actual: 52, optimal: 60 },
  { month: 'Jun', predicted: 67, actual: 65, optimal: 70 },
  { month: 'Jul', predicted: 72, actual: 69, optimal: 75 },
  { month: 'Aug', predicted: 68, actual: 71, optimal: 72 },
  { month: 'Sep', predicted: 63, actual: 60, optimal: 68 },
  { month: 'Oct', predicted: 58, actual: 55, optimal: 62 },
  { month: 'Nov', predicted: 52, actual: 49, optimal: 56 },
  { month: 'Dec', predicted: 47, actual: 44, optimal: 51 }
];

// Stress detection data for pie chart
export const stressDetectionData = [
  { name: 'स्वस्थ (Healthy)', value: 65, color: '#22c55e' },
  { name: 'सूखा (Drought)', value: 20, color: '#f59e0b' },
  { name: 'गर्मी (Heat Stress)', value: 10, color: '#ef4444' },
  { name: 'कीट (Pest)', value: 5, color: '#8b5cf6' }
];

// Weather data
export const weatherData = {
  current: {
    temperature: 28,
    humidity: 65,
    rainfall: 12.5,
    windSpeed: 8.2,
    uvIndex: 6,
    soilMoisture: 45
  },
  forecast: [
    { day: 'आज', temp: 28, condition: 'Partly Cloudy', icon: '⛅' },
    { day: 'कल', temp: 30, condition: 'Sunny', icon: '☀️' },
    { day: 'परसों', temp: 26, condition: 'Rainy', icon: '🌧️' },
    { day: 'शुक्रवार', temp: 29, condition: 'Cloudy', icon: '☁️' },
    { day: 'शनिवार', temp: 31, condition: 'Hot', icon: '🌡️' }
  ]
};

// Fertilizer recommendations
export const fertilizerRecommendations = [
  {
    type: "नाइट्रोजन (Nitrogen)",
    recommended: "120 kg/hectare",
    current: "100 kg/hectare",
    status: "increase",
    advice: "फसल की वृद्धि के लिए नाइट्रोजन बढ़ाएं"
  },
  {
    type: "फास्फोरस (Phosphorus)",
    recommended: "60 kg/hectare",
    current: "65 kg/hectare",
    status: "optimal",
    advice: "वर्तमान मात्रा उपयुक्त है"
  },
  {
    type: "पोटाश (Potash)",
    recommended: "40 kg/hectare",
    current: "50 kg/hectare",
    status: "decrease",
    advice: "पोटाश की मात्रा कम करें"
  }
];

// Regional analytics for admin dashboard
export const regionalAnalytics = [
  { region: 'पंजाब', farmers: 1250, avgYield: 68, stressAlerts: 45 },
  { region: 'उत्तर प्रदेश', farmers: 2100, avgYield: 62, stressAlerts: 78 },
  { region: 'गुजरात', farmers: 890, avgYield: 71, stressAlerts: 32 },
  { region: 'महाराष्ट्र', farmers: 1680, avgYield: 65, stressAlerts: 56 },
  { region: 'राजस्थान', farmers: 750, avgYield: 58, stressAlerts: 89 },
  { region: 'हरियाणा', farmers: 920, avgYield: 69, stressAlerts: 41 }
];

// Sample alerts for farmers
export const sampleAlerts = [
  {
    id: 1,
    type: 'warning',
    icon: '⚠️',
    message: 'मिट्टी में नमी कम है - सिंचाई की आवश्यकता',
    timestamp: '2 घंटे पहले',
    priority: 'high'
  },
  {
    id: 2,
    type: 'info',
    icon: '🌡️',
    message: 'अगले 3 दिन तापमान 35°C से ऊपर रहेगा',
    timestamp: '4 घंटे पहले',
    priority: 'medium'
  },
  {
    id: 3,
    type: 'success',
    icon: '✅',
    message: 'फसल की वृद्धि सामान्य है',
    timestamp: '1 दिन पहले',
    priority: 'low'
  },
  {
    id: 4,
    type: 'warning',
    icon: '🐛',
    message: 'कीट प्रकोप की संभावना - निगरानी रखें',
    timestamp: '2 दिन पहले',
    priority: 'high'
  }
];

// Crop types with icons
export const cropTypes = [
  { name: 'गेहूं', icon: '🌾', season: 'रबी' },
  { name: 'धान', icon: '🌾', season: 'खरीफ' },
  { name: 'मक्का', icon: '🌽', season: 'खरीफ' },
  { name: 'कपास', icon: '🌿', season: 'खरीफ' },
  { name: 'गन्ना', icon: '🎋', season: 'वार्षिक' },
  { name: 'सरसों', icon: '🌻', season: 'रबी' },
  { name: 'चना', icon: '🫘', season: 'रबी' },
  { name: 'सोयाबीन', icon: '🫘', season: 'खरीफ' }
];

// Soil types
export const soilTypes = [
  'Alluvial (जलोढ़)',
  'Black (काली मिट्टी)',
  'Red (लाल मिट्टी)',
  'Laterite (लैटेराइट)',
  'Desert (रेगिस्तानी)',
  'Mountain (पर्वतीय)',
  'Clay Loam (चिकनी दोमट)',
  'Sandy Loam (बलुई दोमट)'
];

// Irrigation types
export const irrigationTypes = [
  'Drip Irrigation (ड्रिप)',
  'Sprinkler (स्प्रिंकलर)',
  'Flood Irrigation (बाढ़ सिंचाई)',
  'Furrow Irrigation (कूंड सिंचाई)',
  'Rain Fed (वर्षा आधारित)',
  'Tube Well (नलकूप)',
  'Canal (नहर)',
  'Tank Irrigation (तालाब)'
];
