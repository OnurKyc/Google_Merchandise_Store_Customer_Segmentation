from google.cloud import bigquery

client = bigquery.Client()

# Perform a query.
QUERY = (
    SELECT date Date, TIMESTAMP_SECONDS(VisitStartTime) VisitStartTime, CONCAT(FullVisitorId, CAST(VisitId AS STRING)) UniqueSessionId, 
    FullVisitorId User,VisitId, VisitNumber, TrafficSource.Source, TrafficSource.Medium,
    Device.DeviceCategory Device, Device.OperatingSystem, Device.Browser, ChannelGrouping Channel, Geonetwork.Region State,
    CAST(SUM(IFNULL(Totals.Transactions,0)) AS INTEGER) AS Orders, 
    CAST(SUM(IFNULL(Totals.PageViews,0)) AS INTEGER) AS PageViews, 
    CAST(SUM(IFNULL(Totals.Visits,0)) AS INTEGER) AS Visits, 
    ROUND(SUM(IFNULL(Totals.TimeOnSite, 0))/60,2) AS DurationMinutes, 
    SUM(IFNULL(Totals.TotalTransactionRevenue, 0))/1000000 As Sales  
    FROM `bigquery-public-data.google_analytics_sample.ga_sessions_*`
    WHERE _TABLE_SUFFIX BETWEEN '20160801' AND '20170801' 
    AND geoNetwork.country = 'Turkey' 
    AND trafficSource.source <> 'mall.googleplex.com'  
    GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12,13
    ORDER BY 3;)


query_job = client.query(QUERY)  # API request
rows = query_job.result()  # Waits for query to finish

for row in rows:
    print(row.name)