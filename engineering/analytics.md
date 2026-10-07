# Website evidence contract

The frontend agent consumes a private provider export or connector response. Hosting alone does not imply analytics or heatmaps are installed.

Daily input: UTC window bounds, provider/source, collection status, pageviews, sessions if measured, referrer categories, device class, page path, click counts by stable element ID, scroll-depth buckets and frontend errors. Include sample size and compare with a same-duration previous window; use a 7-day view for low-volume sites. Record bot/internal-traffic filtering and known gaps.

Clicks and scroll depth are attention proxies, not eye tracking or proof a visitor read a section. Never claim statistical improvement from tiny samples. A hypothesis must name its observation, proposed change, primary metric and evaluation window. At most one experiment at a time per page.

Prefer aggregate click events using stable element IDs and coarse viewport buckets. Do not collect form contents, keystrokes, contact text, raw session replay, full query strings or user identifiers for this first iteration. A spatial click heatmap needs measured coordinates/viewport normalization from an actual integration; do not generate one from screenshots or fabricated data. Keep raw telemetry and private reports out of public repositories.

If collection is missing or stale, report it once and create an instrumentation proposal. Until a real provider/export is configured, design reviews are qualitative and traffic measurements remain unknown. Changes adding instrumentation are reviewed before release just like other frontend changes.
