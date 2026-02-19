export default function PrivacyPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold text-primary-500 mb-8">Privacy &amp; Data Protection</h1>

      <div className="prose prose-gray max-w-none space-y-6">
        <section className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-3">How We Handle Your Data</h2>
          <p className="text-gray-600 leading-relaxed">
            Your property documents contain sensitive personal information. We take data protection
            seriously and comply with the General Data Protection Regulation (GDPR / AVG).
          </p>
        </section>

        <section className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-3">Data Processing</h2>
          <ul className="space-y-2 text-gray-600">
            <li className="flex items-start gap-2">
              <span className="text-primary-500 mt-1 flex-shrink-0">&#8226;</span>
              Documents are stored locally on our servers and are not shared with third parties.
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary-500 mt-1 flex-shrink-0">&#8226;</span>
              Before sending text to AI for analysis, we redact personal identifiers (BSN, phone
              numbers, email addresses, IBAN numbers).
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary-500 mt-1 flex-shrink-0">&#8226;</span>
              External data lookups (BAG, EP-Online, CBS) use only address and postal code
              information that is publicly available.
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary-500 mt-1 flex-shrink-0">&#8226;</span>
              All data access is logged for audit purposes.
            </li>
          </ul>
        </section>

        <section className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-3">Your Rights</h2>
          <ul className="space-y-2 text-gray-600">
            <li className="flex items-start gap-2">
              <span className="text-green-500 mt-1 flex-shrink-0">&#10003;</span>
              <strong>Right to Access:</strong> Export all your data at any time from the analysis
              page.
            </li>
            <li className="flex items-start gap-2">
              <span className="text-green-500 mt-1 flex-shrink-0">&#10003;</span>
              <strong>Right to Erasure:</strong> Delete all your session data permanently with one
              click.
            </li>
            <li className="flex items-start gap-2">
              <span className="text-green-500 mt-1 flex-shrink-0">&#10003;</span>
              <strong>Data Portability:</strong> Download your complete analysis results as JSON.
            </li>
          </ul>
        </section>

        <section className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-3">Data Retention</h2>
          <p className="text-gray-600 leading-relaxed">
            Session data is temporary and is not retained beyond your active session. You can delete
            all data at any time. We do not create user accounts or store data long-term for the
            prototype version.
          </p>
        </section>
      </div>
    </div>
  );
}
