SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [dbo].[SelectAttr] AS
SELECT Jattr.Json_Path, Jattr.ApiID, api.Source,  attr.AttrType
    FROM JsonAttributes as Jattr
    JOIN API as api on api.ApiID = Jattr.ApiID
    JOIN Attribute AS attr on Jattr.AttrID = attr.AttrID
GO
