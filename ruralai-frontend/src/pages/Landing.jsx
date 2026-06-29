import React from 'react';
import LandingNavbar from '../components/LandingNavbar';
import HeroSection from '../components/HeroSection';
import FeaturesSection from '../components/FeaturesSection';
import HowItWorks from '../components/HowItWorks';
import ImpactSection from '../components/ImpactSection';
import CTASection from '../components/CTASection';
import Footer from '../components/Footer';

export default function Landing() {
  return (
    <div className="min-h-screen bg-white dark:bg-gray-900">
      <LandingNavbar />
      <main className="pt-16">
        <HeroSection />
        <FeaturesSection />
        <HowItWorks />
        <ImpactSection />
        <CTASection />
      </main>
      <Footer />
    </div>
  );
}
