-- CREATE DATABASE [WeatherApplication]
-- GO
--
-- USE [WeatherApplication]
-- GO

DROP VIEW IF EXISTS [vAPI]
DROP VIEW IF EXISTS [vLocation]
DROP VIEW IF EXISTS [vCity]
DROP VIEW IF EXISTS [vCityWeather]
DROP VIEW IF EXISTS [vSelectAttr]
GO

DROP TABLE IF EXISTS [CityAPILocation]
DROP TABLE IF EXISTS [WeatherValues]
DROP TABLE IF EXISTS [Weather]
DROP TABLE IF EXISTS [ValueVC]
DROP TABLE IF EXISTS [JSONAttributes]
DROP TABLE IF EXISTS [City]
DROP TABLE IF EXISTS [Attribute]
DROP TABLE IF EXISTS [API]
GO

CREATE TABLE [ValueVC] (
  [ValueVC_ID]   INT PRIMARY KEY IDENTITY (1,1),
  [ValueVarchar] VARCHAR(100)
)
GO

CREATE TABLE [Attribute] (
  [AttrID]   INT PRIMARY KEY IDENTITY (1,1),
  [AttrName] VARCHAR(100),
  [AttrType] VARCHAR(100)
)
GO

CREATE TABLE [API] (
  [APIID]        INT PRIMARY KEY IDENTITY (1,1),
  [APIKey]       VARCHAR(100),
  [Name]         VARCHAR(100),
  [URL]          VARCHAR(200),
  [CurrentCast]  VARCHAR(MAX),
  [ForeCast]     VARCHAR(MAX),
  [Location]     VARCHAR(MAX),
  [APIName]      VARCHAR(30),
  [JSON_Path_CC] VARCHAR(200),
  [JSON_Path_FC] VARCHAR(200),
  [Active]       BIT DEFAULT 1
)
GO

CREATE TABLE [JSONAttributes] (
  [ID]           INT PRIMARY KEY IDENTITY (1,1),
  [AttrID]       INT REFERENCES [Attribute],
  [APIID]        INT REFERENCES [API],
  [JSON_Attr_CC] VARCHAR(100),
  [JSON_Attr_FC] VARCHAR(100)
)
GO

CREATE TABLE [City] (
  [CityID]   INT PRIMARY KEY IDENTITY (1,1),
  [CityName] VARCHAR(100),
  [Active]   BIT DEFAULT 1
)
GO

CREATE TABLE [Weather] (
  [WeatherID]   INT PRIMARY KEY IDENTITY (1,1),
  [QueryDate]   DATETIME,
  [ForecastDay] DATETIME,
  [CityID]      INT REFERENCES [City],
  [APIID]       INT REFERENCES [API]
)
GO

CREATE TABLE [WeatherValues] (
  [ID]          INT PRIMARY KEY IDENTITY (1,1),
  [ValuesInt]   INT,
  [ValuesMoney] MONEY,
  [ValueVC_ID]  INT REFERENCES [ValueVC],
  [WeatherID]   INT REFERENCES [Weather],
  [AttrID]      INT REFERENCES [Attribute]
)
GO

CREATE TABLE [CityAPILocation] (
  [ID]          INT PRIMARY KEY IDENTITY (1,1),
  [APIID]       INT REFERENCES [API],
  [CityID]      INT REFERENCES [City],
  [LocationKey] VARCHAR(MAX)
)
GO

---------------------------------------------------------------------------------------------------
--------  Nézettáblák -----------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------

CREATE OR ALTER VIEW [vCity] AS
  SELECT *
    FROM [City]
    WHERE [Active] = 1
GO

CREATE OR ALTER VIEW [vAPI] AS
  SELECT *
    FROM [API]
    WHERE [Active] = 1
GO

CREATE OR ALTER VIEW [vLocation] AS
  SELECT [a].[APIID], [a].[Name] AS [AName], [c].[CityName] AS [CName], [l].[LocationKey]
    FROM [API] AS [a]
    JOIN [CityAPILocation] AS [l] ON [a].[APIID] = [l].[APIID]
    JOIN [City] AS [c] ON [l].[CityID] = [c].[CityID]
GO

CREATE OR ALTER VIEW [dbo].[vSelectAttr] AS
  SELECT -- [a].[JSON_Path_CC],
         [j].[JSON_Attr_CC],
         -- [a].[JSON_Path_FC],
         ISNULL([j].[JSON_Attr_FC], [j].[JSON_Attr_CC]) AS [JSON_Attr_FC],
         [a].[APIID], -- [a].[Name],
         [t].[AttrType], [t].[AttrID]
    FROM [JSONAttributes] AS [j]
    JOIN [API] AS [a] ON [a].[APIID] = [j].[APIID]
    JOIN [Attribute] AS [t] ON [j].[AttrID] = [t].[AttrID]
GO

CREATE OR ALTER VIEW [dbo].[vCityWeather] AS
  SELECT [w].[ForecastDay], [c].[CityName],
         [a].[Name], [wv].[ValuesInt], [wv].[ValuesMoney], [v].[ValueVarchar],
         [a].[JSON_Path_CC], [j].[JSON_Attr_CC],
         [a].[JSON_Path_FC], ISNULL([j].[JSON_Attr_FC], [j].[JSON_Attr_CC]) AS [JSON_Attr_FC]
    FROM [City] AS [c]
    JOIN      [Weather] AS [w] ON [c].[CityID] = [w].[CityID]
    JOIN      [API] AS [a] ON [a].[APIID] = [w].[APIID]
    JOIN      [JSONAttributes] AS [j] ON [j].[APIID] = [a].[APIID]
    JOIN      [WeatherValues] AS [wv] ON [wv].[WeatherID] = [w].[WeatherID]
    LEFT JOIN [ValueVC] AS [v] ON [wv].[ValueVC_ID] = [v].[ValueVC_ID]
GO

---------------------------------------------------------------------------------------------------
--------  Nézettáblák triggerei -------------------------------------------------------------------
---------------------------------------------------------------------------------------------------

CREATE OR ALTER TRIGGER [tr_CW]
  ON [vCityWeather]
  INSTEAD OF INSERT AS
BEGIN
  INSERT [City] ([CityName])
  SELECT DISTINCT [i].[CityName]
    FROM [inserted] AS [i]
    WHERE [i].[CityName] IS NOT NULL
      AND NOT EXISTS(SELECT 1
                       FROM [City] AS [c]
                       WHERE [c].[CityName] = [i].[CityName])

  INSERT [ValueVC] ([ValueVarchar])
  SELECT DISTINCT [i].[ValueVarchar]
    FROM [inserted] AS [i]
    WHERE [i].[ValueVarchar] IS NOT NULL
      AND NOT EXISTS(SELECT 1
                       FROM [ValueVC] AS [v]
                       WHERE [v].[ValueVarchar] = [i].[ValueVarchar])

  DECLARE @date SMALLDATETIME = GETDATE()
  INSERT [Weather] ([APIID], [CityID], [QueryDate], [ForecastDay])
  SELECT DISTINCT [a].[APIID], [c].[CityID], @date, [i].[ForecastDay]
    FROM [inserted] AS [i]
    JOIN [API] AS [a] ON [a].[Name] = [i].[Name]
    JOIN [City] AS [c] ON [c].[CityName] = [i].[CityName]

  --   INSERT [WeatherValues] ([WeatherID], [AttrID], [ValueVC_ID], [ValuesInt], [ValuesMoney])
--   SELECT DISTINCT [w].[WeatherID], [ja].[AttrID], [v].[ValueVC_ID], [i].[ValuesInt], [i].[ValuesMoney]
--     FROM [inserted] AS [i]
--     JOIN      [API] AS [a] ON [a].[Name] = [i].[Name]
--     JOIN      [City] AS [c] ON [c].[CityName] = [i].[CityName]
--     JOIN      [Weather] AS [w] ON [w].[APIID] = [a].[APIID] AND [w].[CityID] = [c].[CityID] AND [w].[QueryDate] = @date
--     LEFT JOIN [ValueVC] AS [v] ON [i].[ValueVarchar] = [v].[ValueVarchar]
--     LEFT JOIN [JSONAttributes] AS [ja] ON [i].[JSON_Path_CC] = [ja].[JSON_Path_CC]
--         AND [i].[JSON_Attr_CC] = [ja].[JSON_Attr_CC]
END
GO

CREATE OR ALTER TRIGGER [tr_CAL]
  ON [vLocation]
  INSTEAD OF INSERT AS
BEGIN
  INSERT INTO [City] ([CityName])
  SELECT DISTINCT [CName]
    FROM [inserted] AS [i]
    WHERE NOT EXISTS(SELECT 1 FROM [City] AS [c] WHERE [i].[CName] = [c].[CityName])

  INSERT INTO [CityAPILocation] ([APIID], [CityID], [LocationKey])
  SELECT DISTINCT [a].[APIID], [c].[CityID], [i].[LocationKey]
    FROM [inserted] AS [i]
    JOIN [API] AS [a] ON [a].[Name] = [i].[AName]
    JOIN [City] AS [c] ON [c].[CityName] = [i].[CName]
    WHERE NOT EXISTS(SELECT 1
                       FROM [CityAPILocation] AS [l]
                       WHERE [l].[APIID] = [a].[APIID]
                         AND [l].[CityID] = [c].[CityID])
END
GO

---------------------------------------------------------------------------------------------------
--------  Alapadatok ------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------

INSERT INTO [City] ([CityName])
  VALUES ('Ajka'),
         ('Balatonfured'),
         ('Bekescsaba'),
         ('Budaors'),
         ('Budapest'),
         ('Cegled'),
         ('Csorna'),
         ('Debrecen'),
         ('Dunakeszi'),
         ('Dunaujvaros'),
         ('Eger'),
         ('Erd'),
         ('Esztergom'),
         ('Gyor'),
         ('Hatvan'),
         ('Jaszbereny'),
         ('Kaposvar'),
         ('Kecskemet'),
         ('Komarom'),
         ('Kormend'),
         ('Mako'),
         ('Miskolc'),
         ('Nagykanizsa'),
         ('Nyiregyhaza'),
         ('Papa'),
         ('Pecs'),
         ('Salgotarjan'),
         (N'Sárvár'),
         ('Siofok'),
         ('Sopron'),
         ('Szeged'),
         ('Szekesfehervar'),
         ('Szekszard'),
         ('Szolnok'),
         ('Szombathely'),
         ('Tata'),
         ('Tatabanya'),
         ('Tihany'),
         ('Torokbalint'),
         (N'Várpalota'),
         ('Vecses'),
         ('Veszprem'),
         ('Zalaegerszeg')
GO

SET IDENTITY_INSERT [dbo].[API] ON
INSERT [dbo].[API] ([APIID], [APIKey], [Name], [URL], [CurrentCast], [ForeCast], [Location], [APIName],
                    [JSON_Path_CC], [JSON_Path_FC], [Active])
  VALUES (1, 'd43412fab3e9aa840c40c50ad38cc6e9', 'Dark Sky',
          'https://api.darksky.net/forecast/',
          '{url}{apikey}/{location}?&units=ca&lang=en',
          '{url}{apikey}/{location}?&units=ca&lang=en&exclude=daily&extend=hourly',
          '',
          'DarkSky',
          'currently', 'hourly/data',
          1),
         (2, 'G6XBgWa9eLvzcIIRsJj6abhi4OsEXz0k', 'Accu Weather',
          'http://dataservice.accuweather.com/',
          '{url}forecasts/v1/hourly/1hour/{location}?apikey={apikey}&language=en-us&details=true&metric=true',
          '{url}forecasts/v1/daily/5day/{location}?apikey={apikey}&language=en-us&details=true&metric=true',
          '{url}locations/v1/cities/search?apikey={apikey}&q={location},HU&language=en-us',
          'AccuWeather',
          '', 'DailyForecasts',
          1),
         (3, '63f727b2e84f011a46f960fd7e1a3680', 'Open Weather',
          'https://api.openweathermap.org/data/',
          '{url}2.5/weather?q={location},hu&units=metric&appid={apikey}&%22',
          '{url}2.5/forecast?q={location},hu&units=metric&appid={apikey}&%22',
          '',
          'WeatherAPIBase',
          '', 'list',
          1),
         (4, '5bfdc7a7a51841cc9ddb4f35462ae665', 'Weather Bit',
          'https://api.weatherbit.io/v2.0/',
          '{url}current?city={location}&country=HU&tz=local&key={apikey}&units=metric',
          '{url}forecast/daily?city={location}&country=HU&tz=local&key={apikey}&units=metric',
          '',
          'WeatherAPIBase',
          'data', 'data',
          1)
SET IDENTITY_INSERT [dbo].[API] OFF
GO

-- Valós adat - így csökken a kérések száma, ami pl. Accu Weather szempontjából fontos! ;)

INSERT INTO [vLocation] ([AName], [CName], [LocationKey])
  VALUES ('Accu Weather', 'Ajka', '191470'),
         ('Accu Weather', 'Balatonfured', '2-191478_1_AL'),
         ('Accu Weather', 'Bekescsaba', '1-187162_1_AL'),
         ('Accu Weather', 'Budaors', '1-187422_1_AL'),
         ('Accu Weather', 'Budapest', '187423'),
         ('Accu Weather', 'Cegled', '1-189903_1_AL'),
         ('Accu Weather', 'Csorna', '188331'),
         ('Accu Weather', 'Debrecen', '188406'),
         ('Accu Weather', 'Dunakeszi', '189895'),
         ('Accu Weather', 'Dunaujvaros', '1-187918_1_AL'),
         ('Accu Weather', 'Eger', '188467'),
         ('Accu Weather', 'Erd', '1-189896_1_AL'),
         ('Accu Weather', 'Esztergom', '188899'),
         ('Accu Weather', 'Gyor', '1-188380_1_AL'),
         ('Accu Weather', 'Hatvan', '188468'),
         ('Accu Weather', 'Jaszbereny', '1-188606_1_AL'),
         ('Accu Weather', 'Kaposvar', '1-190564_1_AL'),
         ('Accu Weather', 'Kecskemet', '1256185'),
         ('Accu Weather', 'Komarom', '1-188900_1_AL'),
         ('Accu Weather', 'Kormend', '1-191391_1_AL'),
         ('Accu Weather', 'Mako', '1-187686_1_AL'),
         ('Accu Weather', 'Miskolc', '187408'),
         ('Accu Weather', 'Nagykanizsa', '191709'),
         ('Accu Weather', 'Nyiregyhaza', '2-190718_1_AL'),
         ('Accu Weather', 'Papa', '1-191474_1_AL'),
         ('Accu Weather', 'Pecs', '187152'),
         ('Accu Weather', 'Salgotarjan', '1-189569_1_AL'),
         ('Accu Weather', N'Sárvár', '191384'),
         ('Accu Weather', 'Siofok', '1-190566_1_AL'),
         ('Accu Weather', 'Sopron', '188328'),
         ('Accu Weather', 'Szeged', '187706'),
         ('Accu Weather', 'Szekesfehervar', '1-187971_1_AL'),
         ('Accu Weather', 'Szekszard', '1-190888_1_AL'),
         ('Accu Weather', 'Szolnok', '188646'),
         ('Accu Weather', 'Szombathely', '191417'),
         ('Accu Weather', 'Tata', '188903'),
         ('Accu Weather', 'Tatabanya', '1-188929_1_AL'),
         ('Accu Weather', 'Tihany', '191517'),
         ('Accu Weather', 'Torokbalint', '1-1249511_1_AL'),
         ('Accu Weather', N'Várpalota', '191472'),
         ('Accu Weather', 'Vecses', '1-189902_1_AL'),
         ('Accu Weather', 'Veszprem', '1-191469_1_AL'),
         ('Accu Weather', 'Zalaegerszeg', '191710')

GO

SET IDENTITY_INSERT [dbo].[Attribute] ON
INSERT [dbo].[Attribute] ([AttrID], [AttrName], [AttrType])
  VALUES (1, 'Description', 'ValueVarchar'),
         (2, 'Humidity', 'ValuesMoney'),
         (3, 'Pressure', 'ValuesMoney'),
         (4, 'Temperature', 'ValuesMoney'),
         (5, 'Wind Speed', 'ValuesMoney'),
         (6, 'Wind Direction', 'ValuesMoney'),
         (7, 'Cloud', 'ValuesMoney'),
         (8, 'PrecipProbability', 'ValuesMoney'),
         (9, 'PrecipType', 'ValueVarchar')
SET IDENTITY_INSERT [dbo].[Attribute] OFF
GO

SET IDENTITY_INSERT [dbo].[JSONAttributes] ON
-- DarkSky
INSERT [dbo].[JSONAttributes] ([ID], [AttrID], [APIID], [JSON_Attr_CC])
  VALUES (1, 1, 1, 'summary'),
         (2, 2, 1, 'humidity'),
         (3, 3, 1, 'pressure'),
         (4, 4, 1, 'temperature'),
         (5, 5, 1, 'windSpeed'),
         (6, 6, 1, 'windBearing'),
         (7, 7, 1, 'cloudCover'),
         (8, 8, 1, 'precipProbability'),
         (9, 9, 1, 'precipType')

-- AccuWeather
INSERT [dbo].[JSONAttributes] ([ID], [AttrID], [APIID], [JSON_Attr_CC])
  VALUES (11, 1, 2, 'IconPhrase'),
         (12, 2, 2, 'RelativeHumidity'),
--          (13, 3, 2, '-pressure'),
         (14, 4, 2, 'Temperature/Value'),
         (15, 5, 2, 'Wind/Speed/Value'),
         (16, 6, 2, 'Wind/Direction/Degrees'),
         (17, 7, 2, 'CloudCover'),
         (18, 8, 2, 'PrecipitationProbability')
--          (19, 9, 2, '-precipType')

-- OpenWeather
INSERT [dbo].[JSONAttributes] ([ID], [AttrID], [APIID], [JSON_Attr_CC])
  VALUES (21, 1, 3, 'weather/description'),
         (22, 2, 3, 'main/humidity'),
         (23, 3, 3, 'main/pressure'),
         (24, 4, 3, 'main/temp'),
         (25, 5, 3, 'wind/speed'),
         (26, 6, 3, 'wind/deg'),
         (27, 7, 3, 'clouds/all')
--          (28, 8, 3, 'precipProbability'),
--          (29, 9, 3, 'precipType')

-- WeatherBit
INSERT [dbo].[JSONAttributes] ([ID], [AttrID], [APIID], [JSON_Attr_CC])
  VALUES (31, 1, 4, 'weather/description'),
--          (32, 2, 4, 'main/humidity'),
         (33, 3, 4, 'pres'),
         (34, 4, 4, 'temp'),
         (35, 5, 4, 'wind_spd'),
         (36, 6, 4, 'wind_dir'),
         (37, 7, 4, 'clouds')
--          (38, 8, 4, 'precipProbability'),
--          (39, 9, 4, 'precipType')

SET IDENTITY_INSERT [dbo].[JSONAttributes] OFF
GO
