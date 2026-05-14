/**
 * Main App Component
 * React Router setup with professional layout
 */

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import Layout from "./components/layout/Layout";
import { ROUTES } from "./constants";
import ErrorBoundary from "./components/common/ErrorBoundary";

// Lazy load pages for better performance
import { lazy, Suspense } from "react";
import LoadingSpinner from "./components/common/LoadingSpinner";

const Dashboard = lazy(() => import("./pages/Dashboard"));
const DiagnosisPage = lazy(() => import("./pages/DiagnosisPage"));
const ResultsPage = lazy(() => import("./pages/ResultsPage"));
const ReportsPage = lazy(() => import("./pages/ReportsPage"));
const StatusPage = lazy(() => import("./pages/StatusPage"));
const DiseaseGuidePage = lazy(() => import("./pages/DiseaseGuidePage"));
const NotFound = lazy(() => import("./pages/NotFound"));

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

// Loading fallback
const PageLoader = () => (
  <div className="flex items-center justify-center min-h-screen">
    <LoadingSpinner size="lg" text="Loading..." />
  </div>
);

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ErrorBoundary>
        <Router>
          <Layout>
            <Suspense fallback={<PageLoader />}>
              <Routes>
                <Route path={ROUTES.HOME} element={<Dashboard />} />
                <Route path={ROUTES.DIAGNOSIS} element={<DiagnosisPage />} />
                <Route path={ROUTES.RESULTS} element={<ResultsPage />} />
                <Route path={ROUTES.REPORTS} element={<ReportsPage />} />
                <Route path={ROUTES.STATUS} element={<StatusPage />} />
                <Route path="/disease-guide" element={<DiseaseGuidePage />} />
                <Route path="*" element={<NotFound />} />
              </Routes>
            </Suspense>
          </Layout>
        </Router>
      </ErrorBoundary>
    </QueryClientProvider>
  );
}

export default App;
