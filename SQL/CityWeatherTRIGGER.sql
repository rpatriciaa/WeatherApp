CREATE OR ALTER TRIGGER CWTrigger ON CityWeather INSTEAD OF INSERT AS
BEGIN
  INSERT City (CityName)
    SELECT DISTINCT i.CityName
      FROM inserted AS i
      WHERE i.CityName IS NOT NULL
        AND NOT EXISTS(SELECT 1
                        FROM City AS c
                        WHERE c.CityName = i.CityName)
                       
  INSERT ValueVC (ValueVarchar)
    SELECT DISTINCT i.ValueVarchar
    FROM inserted AS i
    WHERE i.ValueVarchar IS NOT NULL
    AND NOT EXISTS(SELECT 1
                      FROM ValueVC AS v
                      WHERE v.ValueVarchar = i.ValueVarchar)

  DECLARE @date SMALLDATETIME = GETDATE()
  INSERT Weather (ApiID,CityID,QueryDate,ForecastDay)
    SELECT DISTINCT a.ApiID, c.CityID, @date, i.ForecastDay
      FROM inserted as i
      JOIN API as a on a.Source = i.Source
      JOIN City as c on c.CityName = i.CityName

  INSERT WeatherValues (WeatherID, AttrID, ValueVC_ID, ValuesInt, ValuesMoney)
    SELECT DISTINCT w.WeatherID, ja.AttrID, v.ValueVC_ID, i.ValuesInt, i.ValuesMoney
      FROM inserted AS i
      JOIN API as a on a.Source = i.Source
      JOIN City as c on c.CityName = i.CityName
      JOIN Weather AS w ON w.ApiID = a.ApiID AND w.CityID = c.CityID AND w.QueryDate = @date
      LEFT JOIN ValueVC AS v ON i.ValueVarchar = v.ValueVarchar
      LEFT JOIN JsonAttributes AS ja ON i.Json_Path = ja.Json_Path
END