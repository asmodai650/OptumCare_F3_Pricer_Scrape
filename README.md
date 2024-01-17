<p><strong>Scrape Queue Name(s): OptumCare Facets F3 Pricer , OptumCare Facets F3 Pricer Low Priority<br /><br /></strong></p>
<p>Development User Story: US285483</p>
<p><strong>Important Notes:</strong>
<li>High Priority queue pulls from specific Tax IDs</li>

<li>Scrape will stop for its user if more than 15 rows within 5 minutes of scrape run-time are written to the results table with NULL OR zero amt_allowed values</li>

<li>Scrape will stop for its user if more than 10 rows within 5 minutes of scrape run-time are written to the results table for that person with error_type of 'try except failed cannot find claim'</li></p>
<p>

<p><strong>Scrape Starts at:</strong>
<ul>
<li>Facets Main Screen - Scrape will automatically maximize screen and move Citrix window to new workspace</li>
</ul>
</li></p>
<p><strong>Results are written to:</strong>
<ul>
<li>WP000075696.RacerResearch.[DBDataAnalytics-DM].OptumCare_Facets_F3_Pricer_Results</li>
</ul>
</li>

</p>
