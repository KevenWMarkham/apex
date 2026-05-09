export default function Catalog() {
  return (
    <section>
      <h1 className="text-2xl font-bold">Service Catalog</h1>
      <p className="text-sm text-gray-600">
        Browse all 724 scenarios across 38 service codes and 7 industries.
        Filter by industry, domain, service code, featured status. Click a
        scenario to see its 24-step chain and 6-agent fleet.
      </p>
      {/* TBD: fetch /api/catalog/scenarios with filters; render with shadcn DataTable */}
    </section>
  );
}
