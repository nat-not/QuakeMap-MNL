# QuakeMap MNL

QuakeMap MNL is an educational earthquake and evacuation-routing simulator for Discrete Structures 2 at the University of Makati. It focuses on Quezon City, Marikina, Pasig, Makati, Taguig, and Muntinlupa.

Project team · Aaron Gerald Abiera, Jurie Aplaca, Nathaniel Babalcon, Hexel John Ventura, and Rommel Villanueva.

**For classroom use only.** Simulated failures and routes are hypothetical. During a real earthquake, follow your local government, [PHIVOLCS](https://www.phivolcs.dost.gov.ph/), and [NDRRMC](https://ndrrmc.gov.ph/).

## Run locally

Double-click `START-WINDOWS.bat` on Windows, or run this from the project root with Python 3:

```sh
python run_local.py
```

The launcher opens `http://localhost:8080` or the next available port. Serve the folder over HTTP so that the browser can load the JSON and JavaScript modules. The site uses plain HTML, CSS, JavaScript, and a local copy of Leaflet 1.9.4. Online OpenStreetMap tiles add street-level basemap detail. The bundled graph, waterways, mapped boundaries, simulation, and routing work when those tiles are unavailable.

## Classroom walkthrough

1. In **Simulation**, select **Try a sample scenario**. It loads M 5.0, seed `QUAKE-2026`, a Quezon City origin, a group of four, and default shelter settings. The During phase displays protective guidance and suspends routing. After shaking, use the guided actions to inspect a failed road or show a surviving route.
2. Open **Evacuation** to inspect the shortest eligible destination, routes to other demo shelters, or an alternate surviving path to the selected shelter. Enter a different group size, close a shelter, or edit its modeled occupancy. The planner recalculates automatically.
3. Select a road or shelter on the map to inspect it without leaving the current view. In **Network**, use the text-based feature picker to inspect failed segments, graph bridges, and critical junctions, or search a road to view its OSM way and sampled draw.
4. Set a new magnitude and select **Shake network** to run it. Keep the seed fixed for a same-draw comparison. **Run comparison** shows the last two distinct seed/magnitude pairs. **Replay** reruns the latest seed, magnitude, and road overrides.
5. Run **100 trials** to examine average failures and origins with access. Enter **Recovery** and reopen a failed segment to see changes in components, study-origin shelter access, and shortest modeled distance.
6. **Export** saves the completed scenario as JSON. **Import** restores it on a matching graph version and recomputes failures, connectivity, and routing from the saved inputs. Moving an export to a different graph version requires rerunning that scenario on the new graph.

## Geographic data and licensing

- **Modeled network** · [OpenStreetMap France Metro Manila PBF](https://download.openstreetmap.fr/extracts/asia/philippines/) with a snapshot timestamp of 2026-11-17 00:11:34 UTC. The bounded graph keeps the largest connected component of selected major-road classes and connectors. It can include roads through adjoining jurisdictions that join the six study cities. Original node IDs connect ways at mapped junctions. Every simulated segment retains its OSM way ID, geometry, and a geographic distance based on all vertices. The extract omits neighborhood roads outside the selected road classes.
- **Map context** · OpenStreetMap supplies the basemap, six study city boundary polygons, and river/canal geometry. The complete [Taguig relation](https://www.openstreetmap.org/relation/184776) supplements the regional extract. Boundary and barangay labels reflect OSM coverage.
- **Demo shelters** · The markers sit at mapped road junctions. Shelter names, locations as facilities, occupancy, capacity, and operational status are demonstration assumptions. A mapped barangay is shown where a source polygon locates the junction. The site does not use a verified shelter inventory.
- **Fault information** · Consult the [PHIVOLCS GeoHazards Portal and FaultFinder](https://gisweb.phivolcs.dost.gov.ph/) for the official trace. A fault layer is not embedded because the official geometry could not be verified for reuse in this build.

The derived `data/road-network.json` database is available under [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/), © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright). Leaflet is distributed under the license in `vendor/leaflet/LICENSE`. The web app requests standard [OpenStreetMap tiles](https://operations.osmfoundation.org/policies/tiles/) only for the displayed viewport. For heavier public deployment, configure a suitable tile provider in `src/map.js`.

### Rebuild the geographic snapshot

Download the Metro Manila PBF and the complete [Taguig OSM relation XML](https://api.openstreetmap.org/api/0.6/relation/184776/full). Install the preprocessing dependency and generate the browser asset:

```sh
python -m pip install osmium==4.3.2
python tools/build_road_network.py metro_manila-latest.osm.pbf --source-url https://download.openstreetmap.fr/extracts/asia/philippines/metro_manila-latest.osm.pbf --boundary-source taguig.osm
```

The recorded source timestamp and content-derived graph version distinguish data revisions. Replay depends on the graph version, magnitude, seed, and manual overrides. A refreshed PBF may create different results for the same seed. The original synthetic JSON files and generator remain as fixtures for the original algorithm tests.

## Mathematical model and project report

Chapter 2's independent Bernoulli rule is unchanged. For magnitude $M$, a road's failure probability is $0.04 + 0.08(M - 5)$ and an OSM-tagged physical bridge's is $0.10 + 0.13(M - 5)$. Both are clamped to $[0, 0.8]$. Graph traversal identifies connected components, iterative Tarjan finds articulation points and graph bridges, and heap-based Dijkstra ranks eligible destinations by surviving distance. The finite state machine remains Before → During → After → Recovery, with routing available in After and Recovery.

For the report, update Chapter 2's **representation and units** to describe OSM junctions, parallel mapped segments, and geographic polyline lengths in kilometers. Update Chapter 3's **data provenance, graph size, and UI design** to describe the regional extract, map workspace, demonstration shelter assumptions, and routing/search interactions. The earlier 40–60 vertex target describes the proposed classroom graph. The current mapped graph has 9,891 junctions and 12,019 segments, with a smaller set of study origins for access summaries. The segment-level trials use the same formula on a finer graph, so results from the previous schematic and the new graph are not directly comparable.

The network is educational and undirected. It does not check one-way restrictions, turns, pedestrian access, engineering conditions, shaking intensity at a site, or real-time service. The camera motion illustrates the During phase and does not represent a seismic wave or measured acceleration.

## Verification

```sh
npm test
```

Node.js 18+ runs the mathematical and map-data tests. For optional browser integration checks, launch the application in another terminal, install Playwright with `npm install --no-save --package-lock=false playwright`, and run `npm run test:browser` with Google Chrome installed. The browser checks use port 8080 by default. Set `QUAKEMAP_URL` for another local URL, or `QUAKEMAP_BROWSER=msedge` for Microsoft Edge.

## Source layout

- `index.html` and `styles.css` define the workspace, responsive layout, and accessibility styles.
- `src/app.js` coordinates views, scenario playback, and planning.
- `src/map.js` renders Leaflet map geometry, interactive overlays, and shelter clusters.
- `src/network.js`, `src/graph.js`, `src/routing.js`, `src/probability.js`, and `src/scenario.js` contain model logic.
- `src/network-worker.js` runs trials and alternate-path searches in a browser worker.
- `src/scenario-file.js` validates version, graph references, and scenario inputs before import.
#   Q u a k e M a p M N L  
 