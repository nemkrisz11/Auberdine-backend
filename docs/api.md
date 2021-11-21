# Routes

| method | content-type | parameters  | return obj | desc | dev | done |
| :---- | :-------: | :---: | :----: | :---- | :---- | :---: |
| POST /user/register | form-data | [name,email,password] | [name: [String], email: [String], password: [String]] | error messages are in returned strings| Németh Krisztián | &check; | 
| POST /user/login | form-data | [email, password] | [email: [String], password: [String]| JWT returned in body, returned values store error messages | Németh Krisztián | &check; | 
| POST /user/logout | - | - | [msg: String] | "ok" returned if succeed| Németh Krisztián | &check; | 
| GET /user/recommendations | application/json | [count: Int]| [recommendations: Place[] ] | Get list of recommendations | Tremmel Márton | &cross; |
| GET /place/{place_id} | - | - | [PlaceDetails] | | Tremmel Márton | &cross; | 
| POST /place/rate/ | application/json | [place_id: String, rating: integer, description: String] | [msg: String] | | Tremmel Márton | &cross; | 
| GET /user/{user_id} | - | - | [username, places: Place[]] | All places the user has rated. friend_ratings property contains user rating | Németh Krisztián | &cross; | 
| GET /user/properties/ | - | - | [user: UserProperties] |  | Németh Krisztián | &check; | 
| POST /user/properties/ | application/json | [name (opt), password] | [new_name: [String], new_password: [String], password: [String]] | Change name and password. Requires additional password auth. Returned fields store errors | Németh Krisztián | &check; |
| GET /user/friends/ | - | - | [friends: User[]] | get friends of the user | Borsodi Regő | &check; |
| DELETE /user/friends/ | application/json |[friend_id: String] | [msg: String] | "ok" if no error| Borsodi Regő | &check; |
| GET /user/friend_requests/ | - | - | [friend_requests: User[]] | | Borsodi Regő | &check; |
| POST /user/friend_requests/ | application/json | [user_id: String, accepted: bool] | [msg: String] | "ok" if no error| Borsodi Regő | &check; |
| POST /user/search/ | application/json | [query: String] | [users: User[]] | | Borsodi Regő | &check; |
| POST /user/friend_request/ | application/json | [user_id: String] | [msg: String] | "ok" if no error | Borsodi Regő | &check; |



# Schemas

## UserProperties

| property | type | desc |
| ---- | ---- | ---- |
| name | String	| user name |
| email | String | user email |

## User
| property | type | desc |
| ---- | ---- | ---- |
| user_id | String | user id |
| name | String	| user name |


## Place

| property | type | desc |
| ---- | ---- | ---- |
| place_id | String | |
| name | String | displayed name of the place |
| picture | String | URL of picture |
| rating | Double | |
| friend_ratings | [Rating] | at most three friend ratings of the place|

## PlaceDetails

| property | type | desc |
| ---- | ---- | ---- |
| name | String | displayed name of the place |
| pictures | String[] | array of picture URLs |
| address | String | |
| website | String | |
| location | [Double, Double] | latitude and longitude of the location |
| rating | Double | |
| friend_ratings | [RatingDetails] | 


## Rating
| property | type | desc |
| ---- | ---- | ---- |
| rating | Int | |
| name | String | |


## RatingDetails
| property | type | desc |
| ---- | ---- | ---- |
| user_id | String | user id in database |
| rating | Int | |
| name | String | |
| description | String |  |

# Authorization

- JWT header: ["alg": "HS256", "typ": "JWT"]
- JWT payload properties: [user_id, timestamp]
- If not authorized, return 401