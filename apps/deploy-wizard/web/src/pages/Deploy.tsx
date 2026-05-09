export default function Deploy() {
  return (
    <section>
      <h1 className="text-2xl font-bold">Deploy</h1>
      <ol className="list-decimal pl-6 space-y-2">
        <li>Pick tenant.</li>
        <li>Pick wave (W1 Foundation · W2 Pilot · W3 Scale & Fuse).</li>
        <li>Pick service codes (multi-select).</li>
        <li>For each service, pick featured scenarios.</li>
        <li>Review the rendered Bicep parameters.</li>
        <li>Run <code>what-if</code>; review the diff.</li>
        <li>Confirm to deploy.</li>
      </ol>
      {/* TBD: WaveStepper component drives the flow; final step POST /api/deployments */}
    </section>
  );
}
