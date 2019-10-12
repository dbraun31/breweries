import sys
sys.path.append('01-DefineCompetitionRegions/')
sys.path.append('02-MatchCompetitionRegionsToZips/')
import DefineCompetitionAreas as dca
import ReverseGeocode as rgc


centroids = dca.main()

centroid_data = rgc.main(centroids)

## save to file
f = open('../Phase1-FindSimilarCompetitionRegions/data/centroid_data.txt', 'w')
f.write(str(centroid_data))
f.close()