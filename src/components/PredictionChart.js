import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const PredictionChart = ({ prediction }) => {
  const featureData = [
    { name: 'Credit Score', impact: prediction.prediction === 'Very_Good' ? 85 : prediction.prediction === 'Normal' ? 65 : 35 },
    { name: 'Payment History', impact: prediction.prediction === 'Very_Good' ? 90 : prediction.prediction === 'Normal' ? 70 : 40 },
    { name: 'Debt Ratio', impact: prediction.prediction === 'Very_Good' ? 80 : prediction.prediction === 'Normal' ? 60 : 30 },
    { name: 'Credit Length', impact: prediction.prediction === 'Very_Good' ? 75 : prediction.prediction === 'Normal' ? 55 : 25 },
    { name: 'Fluctuations', impact: prediction.prediction === 'Very_Good' ? 70 : prediction.prediction === 'Normal' ? 50 : 20 }
  ];

  const confidenceData = [
    { name: 'Confidence', value: parseFloat(prediction.confidence) },
    { name: 'Uncertainty', value: 100 - parseFloat(prediction.confidence) }
  ];

  const COLORS = ['#22c55e', '#ef4444'];

  return (
    <div className="space-y-6">
      {/* Feature Impact Bar Chart */}
      <div>
        <h4 className="text-lg font-medium mb-3 text-gray-900 dark:text-white">
          Feature Impact Scores
        </h4>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={featureData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="name" 
              tick={{ fontSize: 12 }}
              angle={-45}
              textAnchor="end"
              height={80}
            />
            <YAxis />
            <Tooltip />
            <Bar 
              dataKey="impact" 
              fill={prediction.prediction === 'Very_Good' ? '#22c55e' : prediction.prediction === 'Normal' ? '#f59e0b' : '#ef4444'}
              radius={[4, 4, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Confidence Pie Chart */}
      <div>
        <h4 className="text-lg font-medium mb-3 text-gray-900 dark:text-white">
          Prediction Confidence
        </h4>
        <ResponsiveContainer width="100%" height={200}>
          <PieChart>
            <Pie
              data={confidenceData}
              cx="50%"
              cy="50%"
              innerRadius={40}
              outerRadius={80}
              paddingAngle={5}
              dataKey="value"
            >
              {confidenceData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index]} />
              ))}
            </Pie>
            <Tooltip formatter={(value) => `${value}%`} />
          </PieChart>
        </ResponsiveContainer>
        <div className="flex justify-center space-x-4 mt-2">
          <div className="flex items-center">
            <div className="w-3 h-3 bg-success-500 rounded-full mr-2"></div>
            <span className="text-sm">Confidence ({prediction.confidence}%)</span>
          </div>
          <div className="flex items-center">
            <div className="w-3 h-3 bg-danger-500 rounded-full mr-2"></div>
            <span className="text-sm">Uncertainty ({(100 - parseFloat(prediction.confidence)).toFixed(1)}%)</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PredictionChart;