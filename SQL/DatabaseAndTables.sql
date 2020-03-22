
USE WeatherApplication

CREATE TABLE ValueVC(
    ValueVC_ID INT PRIMARY KEY IDENTITY(1,1),
    ValueVarchar VARCHAR(100)
)

CREATE TABLE Attribute
(
    AttrID INT PRIMARY KEY IDENTITY(1,1),
    AttrName VARCHAR(100),
    AttrType VARCHAR(100)
)
CREATE TABLE API(
    ApiID INT PRIMARY KEY IDENTITY(1,1),
    ApiKey VARCHAR(100),
    Source VARCHAR(100)
)
CREATE TABLE JsonAttributes(
    ID INT PRIMARY KEY IDENTITY(1,1),
    AttrID INT FOREIGN KEY REFERENCES Attribute(AttrID),
    ApiID INT FOREIGN KEY REFERENCES API(ApiID),
    Json_Path VARCHAR(100)

)
CREATE TABLE City (
    CityID INT PRIMARY KEY IDENTITY(1,1),
    CityName VARCHAR(100)
)

CREATE TABLE Weather(
    WeatherID INT PRIMARY KEY IDENTITY(1,1),
    QueryDate DATETIME,
    ForecastDay DATETIME,
    CityID INT FOREIGN KEY REFERENCES City(CityID),
    ApiID INT FOREIGN KEY REFERENCES API(ApiID)

)

CREATE TABLE WeatherValues(
    ID INT PRIMARY KEY IDENTITY(1,1),
    ValuesInt INT,
    ValuesMoney MONEY,
    ValueVC_ID INT FOREIGN KEY REFERENCES ValueVC(ValueVC_ID),
    WeatherID INT FOREIGN KEY REFERENCES Weather(WeatherID),
    AttrID INT FOREIGN KEY REFERENCES Attribute(AttrID)
)