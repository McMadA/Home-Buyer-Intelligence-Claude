import { Link } from 'react-router-dom';

export default function Footer() {
  return (
    <footer className="bg-gray-100 border-t border-gray-200 py-6 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between text-sm text-gray-500">
        <p>Home Buyer Intelligence Engine</p>
        <Link to="/privacy" className="hover:text-primary-500 transition-colors">
          Privacy &amp; GDPR
        </Link>
      </div>
    </footer>
  );
}
