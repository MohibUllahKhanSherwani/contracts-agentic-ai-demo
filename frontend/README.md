# Daleel Petroleum - Contract Evaluation Dashboard

Enterprise-grade React dashboard for viewing contract evaluation results from the Agentic AI system.

## Features

✅ **Live Data Fetching** - Connects to backend API (GET /results)  
✅ **Auto-refresh** - Updates every 30 seconds automatically  
✅ **Performance Visualization** - Bar chart showing vendor scores  
✅ **Risk Distribution** - Pie chart showing risk levels  
✅ **Sortable Table** - Click column headers to sort  
✅ **Statistics Cards** - Quick metrics overview  
✅ **Responsive Design** - Works on desktop, tablet, mobile  
✅ **Dark Theme** - Modern, professional UI with Tailwind CSS  

---

## Prerequisites

- Node.js 18+ and npm
- Backend API running on `http://localhost:8000`

---

## Installation

```bash
cd frontend
npm install
```

---

## Running the Dashboard

### 1. Start Backend API (in separate terminal)

```bash
# From project root
cd d:\Projects\daleel-petro-contracts-agent
python src\app.py
```

Backend should be running on port 8000.

### 2. Start Frontend Dev Server

```bash
# In frontend directory
npm run dev
```

Dashboard will open at: **http://localhost:3000**

---

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ContractTable.jsx     # Sortable table component
│   │   ├── StatsCard.jsx         # Statistics cards
│   │   ├── PerformanceChart.jsx  # Bar chart visualization
│   │   └── RiskHeatmap.jsx       # Pie chart visualization
│   ├── services/
│   │   └── api.js                # **API CALLS HAPPEN HERE**
│   ├── App.jsx                   # Main dashboard component
│   ├── main.jsx                  # React entry point
│   └── index.css                 # Tailwind CSS styles
├── index.html
├── package.json
├── vite.config.js                # Includes API proxy config
└── tailwind.config.js
```

---

## API Integration

### Where API Calls Happen

**File**: `src/services/api.js`

```javascript
// Fetches contract evaluations from backend
export const fetchEvaluations = async () => {
  const response = await fetch('/api/results');  // Proxied to localhost:8000
  const data = await response.json();
  return data.results || [];
};
```

**File**: `src/App.jsx`

```javascript
// Main component loads data on mount
useEffect(() => {
  loadContracts();  // Calls fetchEvaluations()
}, []);

// Auto-refresh every 30 seconds
useEffect(() => {
  const interval = setInterval(() => {
    loadContracts();
  }, 30000);
  return () => clearInterval(interval);
}, []);
```

### API Endpoints Used

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/results` | GET | Fetch all contract evaluations |
| `/results/{id}` | GET | Fetch specific contract (future use) |
| `/audit-log` | GET | Fetch audit trail (future use) |

---

## Features Explained

### 1. Statistics Cards

Shows:
- Total Contracts
- Low Risk count
- Medium Risk count
- High Risk count
- Average Performance Score

### 2. Performance Bar Chart

- X-axis: Vendor names
- Y-axis: Performance scores (0-100)
- Color-coded by risk level:
  - **Green**: Low risk
  - **Yellow**: Medium risk
  - **Red**: High risk

### 3. Risk Pie Chart

- Shows distribution of risk levels
- Percentage breakdown
- Interactive tooltips

### 4. Contracts Table

- **Sortable columns** (click headers)
- **Color-coded**:
  - Grades: A (green) → F (red)
  - Risk badges: Low/Medium/High
  - Recommendations: RENEW (green), RENEGOTIATE (yellow), TERMINATE (red)
- **Hover effects** for better UX

---

## Customization

### Change Refresh Interval

Edit `src/App.jsx`:

```javascript
// Change 30000 (30 seconds) to desired milliseconds
setInterval(loadContracts, 30000);
```

### Change API Base URL

Edit `vite.config.js`:

```javascript
proxy: {
  '/api': {
    target: 'http://localhost:8000',  // Change port if needed
    // ...
  }
}
```

### Customize Colors

Edit `tailwind.config.js`:

```javascript
colors: {
  'daleel': {
    500: '#0ea5e9',  // Primary brand color
    // Add more shades...
  }
}
```

---

## Build for Production

```bash
npm run build
```

Output will be in `dist/` folder.

Serve with:
```bash
npm run preview
```

---

## Troubleshooting

### Issue: "Failed to fetch evaluations"

**Solution**: Make sure backend API is running on port 8000.

```bash
# Check if API is running
curl http://localhost:8000/health
```

### Issue: CORS errors

**Solution**: Backend already has CORS configured for `http://localhost:3000`. If using different port, update `src/app.py`:

```python
allow_origins=["http://localhost:3000"]
```

### Issue: Charts not showing

**Solution**: Make sure contracts have been evaluated. Run:

```bash
curl -X POST http://localhost:8000/evaluate-sample/abc
curl -X POST http://localhost:8000/evaluate-sample/xyz
curl -X POST http://localhost:8000/evaluate-sample/problematic
```

---

## Demo Walkthrough

1. **Start Backend**: `python src\app.py`
2. **Evaluate Sample Contracts**: Use API or demo script
3. **Start Frontend**: `npm run dev`
4. **Open Browser**: http://localhost:3000
5. **View Dashboard**: See live contract evaluations
6. **Click Refresh**: Manual data reload
7. **Sort Table**: Click column headers
8. **Hover Charts**: See detailed tooltips

---

## Technologies Used

- **React** 18.2 - UI framework
- **Vite** 5.0 - Build tool (fast!)
- **Tailwind CSS** 3.3 - Styling
- **Recharts** 2.10 - Charts/visualizations
- **Lucide React** - Icons

---

## Future Enhancements

- [ ] Expandable table rows with KPI details
- [ ] Audit log viewer
- [ ] Real-time evaluation (WebSocket)
- [ ] Export to Excel/PDF
- [ ] Dark/Light theme toggle
- [ ] Advanced filtering and search
- [ ] Historical trend analysis

---

## Contact

For issues or questions, refer to the main project README.
