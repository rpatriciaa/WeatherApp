SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE   VIEW [dbo].[CityWeather] AS
SELECT w.ForecastDay,c.CityName, a.Source, wv.ValuesInt,wv.ValuesMoney, v.ValueVarchar,ja.Json_Path
    FROM City as c
    JOIN Weather as w on c.CityID = w.CityID
    JOIN Api as a on a.ApiID = w.ApiID
    JOIN JsonAttributes as ja on ja.ApiID = a.ApiID
    JOIN WeatherValues AS wv on wv.WeatherID = w.WeatherID
    LEFT JOIN ValueVC AS v ON wv.ValueVC_ID = v.ValueVC_ID
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
