db.createCollection("users");

/**
 * Initialize users
 */

users = [
    {
        "name": "Pista1",
        "password": "$argon2id$v=19$m=102400,t=2,p=8$tg+GnUCDlEXV0U1fRx8olg$Iehyz46ePynJp/NluKrQGQ", // "kutyafasz"
        "email": "pista1@x.y",
        "friends": [],
        "friend_requests": []
    },
    {
        "name": "Pista2",
        "password": "$argon2id$v=19$m=102400,t=2,p=8$Mdpr+stiIjPrz3FwSyFNJg$sqI8KiCJSY+yBdog2tfAJQ", // "12345678"
        "email": "pista2@x.y",
        "friends": [],
        "friend_requests": []
    },
    {
        "name": "Dr. Goldschmidt Balázs",
        "password": "$argon2id$v=19$m=102400,t=2,p=8$Mdpr+stiIjPrz3FwSyFNJg$sqI8KiCJSY+yBdog2tfAJQ", // "12345678"
        "email": "goldschmidt@iit.bme.hu",
        "friends": [],
        "friend_requests": []
    },
    {
        "name": "John von Neumann",
        "password": "$argon2id$v=19$m=102400,t=2,p=8$Mdpr+stiIjPrz3FwSyFNJg$sqI8KiCJSY+yBdog2tfAJQ", // "12345678"
        "email": "neumann@x.z",
        "friends": [],
        "friend_requests": []
    },
    {
        "name": "Isaac Newton",
        "password": "$argon2id$v=19$m=102400,t=2,p=8$Mdpr+stiIjPrz3FwSyFNJg$sqI8KiCJSY+yBdog2tfAJQ", // "12345678"
        "email": "newton@gravity.org",
        "friends": [],
        "friend_requests": []
    },
    {
        "name": "Vladimir Putin",
        "password": "$argon2id$v=19$m=102400,t=2,p=8$Mdpr+stiIjPrz3FwSyFNJg$sqI8KiCJSY+yBdog2tfAJQ", // "12345678"
        "email": "vlad@kreml.ru",
        "friends": [],
        "friend_requests": []
    }
];
db.users.insertMany(users);

/**
 * Initialize friends of users
 */

pista1 = db.users.findOne({"email":"pista1@x.y"});
pista2 = db.users.findOne({"email":"pista2@x.y"});
goldschmidt = db.users.findOne({"email":"goldschmidt@iit.bme.hu"});
neumann = db.users.findOne({"email":"neumann@x.z"});
newton = db.users.findOne({"email":"newton@gravity.org"});
putin = db.users.findOne({"email":"vlad@kreml.ru"});

db.users.updateOne({"email": pista1.email}, {"$set": {"friends": [pista2._id, goldschmidt._id]}});
db.users.updateOne({"email": pista2.email}, {"$set": {"friends": [pista1._id]}});
db.users.updateOne({"email": goldschmidt.email}, {"$set": {"friends": [pista1._id]}});
db.users.updateOne({"email": neumann.email}, {"$set": {"friends": [newton._id]}});
db.users.updateOne({"email": newton.email}, {"$set": {"friends": [neumann._id]}});

/**
 * Initialize friend requests of users
 */

db.users.updateOne({"email": newton.email}, {"$set": {"friend_requests": [putin._id]}});
db.users.updateOne({"email": neumann.email}, {"$set": {"friend_requests": [pista1._id, pista2._id]}});

/**
 * Initialize places
 */
db.createCollection("places");

places = [
{  "google_place_id" : "ChIJa6hBF8XdQUcROxJNKIQJBRg", "last_sync" : ISODate("2021-11-19T10:31:27.030Z"), "name" : "Rubin Wellness & Conference Hotel", "address" : "Budapest, Dayka Gábor utca 3", "location" : { "type" : "Point", "coordinates" : [ 47.472167, 19.0201056 ] }, "pictures" : [ "Aap_uEBfxVG2U_3FHYmzLx5GXO04sO0I2e5b1g1JzBO9zgRW5asMDffCAtDONBhzoFG1YxeLY5Ke3jvAzWBSBFAQil1ow_9x27WAoxNAXQaTjPAirxf1CKSU5bNrEMZKnRey2mnqOccPgb6lhf1jTfD0Zd7Krk_bjjA6Xp-R_uVCAQgJcUUe" ] },
{  "google_place_id" : "ChIJz6ybSx_cQUcR1_F51gsnSr4", "last_sync" : ISODate("2021-11-19T10:31:27.033Z"), "name" : "St. George Residence", "address" : "Budapest, Fortuna utca 4", "location" : { "type" : "Point", "coordinates" : [ 47.503334, 19.0318289 ] }, "pictures" : [ "Aap_uEDrggq1JL-x0tWcxRutRVtBvYxa69gdSQrK1kI9m0bNP2WmeF2PFPEuCOyJIdMGwrPRzTkV077uWXS13-uG_Og0zv3BS4nWWXUflKJuJ0rKRP1wkelQQOfGlYRfc1tQdU4LOH5014k7CI9ja8M4lCLmZz4ULk0I9EqRfT4SwPtEumec" ] },
{  "google_place_id" : "ChIJt2RniRfcQUcRpiij772lJOw", "last_sync" : ISODate("2021-11-19T10:31:27.035Z"), "name" : "art'bistrobar", "address" : "Budapest, Bem rakpart 16", "location" : { "type" : "Point", "coordinates" : [ 47.502741, 19.039448 ] }, "pictures" : [ "Aap_uEDk7X7G7nDvtaomoP1XkEL9bMThWYZo9UO8BfAWtxCAANXUGWEexRDiw3X9Z0_ADq6MoJgl9unuuFyfHqFRd5NJwIzfDOflLCx5mgcycPp3ZsbctAeQ4G8qh588OGCCCm7QsQ5oGm_ws_iCbfBPe7mHAv3Ws71yeaLeyKp9yR8c9co8" ] },
{  "google_place_id" : "ChIJS3lyakDcQUcRhHOxez3aqUA", "last_sync" : ISODate("2021-11-19T10:31:27.036Z"), "name" : "Kempinski Hotel Corvinus Budapest", "address" : "Budapest, Erzsébet tér 7-8", "location" : { "type" : "Point", "coordinates" : [ 47.4973877, 19.0522634 ] }, "pictures" : [ "Aap_uEAZ-gQwJ7isynEufdvqVn_yof6bvOY7MWb3LhkQejZgJ8hvy2X9M3LCdo1q-O9JAduUQJXzFPARZM112DIeNCd5mhjn_2wzH7KhpbOJe7eUT3EXwHka3PcnnZcSd09E3XaPr4haX0DnEqcMO7ry1HGMptWS-AYRY-_sC6zNkjXUFjLb" ] },
{  "google_place_id" : "ChIJceAajRfcQUcRDVkN0SLIKHQ", "last_sync" : ISODate("2021-11-19T10:31:27.037Z"), "name" : "art'otel budapest", "address" : "Budapest, Bem rakpart 16-19", "location" : { "type" : "Point", "coordinates" : [ 47.502596, 19.039576 ] }, "pictures" : [ "Aap_uEAsr_pK2QWiC95bJNZr682r3i1CnLE6RTz9WZhX3eS_HCEJWCwtB5K0Mu6xN8Jf9wpLEuJOQ4VZUZvckG7rqreFYTbn1qVCiF7_R08h8yNl3XJOA4m1UjFpaFeudoGUDvVU0ikJelILzclC7jtsNmM4yyft8ymvca3Y-yGuex_Mo9oo" ] },
{  "google_place_id" : "ChIJdw64tKDeQUcRD62_jsDPN1M", "last_sync" : ISODate("2021-11-19T10:31:27.039Z"), "name" : "Mammut", "address" : "Budapest, Lövőház utca 2-6", "location" : { "type" : "Point", "coordinates" : [ 47.5083919, 19.0261295 ] }, "pictures" : [ "Aap_uEBNlLmQ7Xhxj6hZaasUwzG3io98R2RO6n0eJycF6kRla5eNBRd_Ndii7Vb_H2AxpsgBFGlSRwiJFerK-IXO8rswNfimliaJQCwh5NTCWmjElxl_Pv1mCMeLu0WYTGA_-4PMrKGDXNVOytUHqPBit1owjqdCGSZ-fj7jh-EfPkE8Tgwe" ] },
{  "google_place_id" : "ChIJ_UtEmincQUcRfmrMihpcE90", "last_sync" : ISODate("2021-11-19T10:31:27.040Z"), "name" : "Larus Étterem", "address" : "Budapest, Csörsz utca 18/b", "location" : { "type" : "Point", "coordinates" : [ 47.49015199999999, 19.019018 ] }, "pictures" : [ "Aap_uEDCBGxVugZIYyUiPUZdDIp8Is_dKh_gEndoIn8FbmOVLJ0tTwbVDtwvM42d-kVa9ZMlkvSwxmALnMmrp4laxq4iHnXaAe7CX0iGuWCrZMiJhK0Ola5G7oGJHElJPlqPqpfslLkL0j5lqS9XgRcd5Sw_PGHR2nzE7Uz-HDUQoJ_agglu" ] },
{  "google_place_id" : "ChIJ2_ro3qbeQUcRNEnJQ8Slre0", "last_sync" : ISODate("2021-11-19T10:31:27.042Z"), "name" : "Márkus és Társa Bt.", "address" : "Budapest, Lövőház utca 17", "location" : { "type" : "Point", "coordinates" : [ 47.50974009999999, 19.0252484 ] }, "pictures" : [ ] },
{  "google_place_id" : "ChIJeQACh0DcQUcRVO6JctVQ5-g", "last_sync" : ISODate("2021-11-19T10:31:27.043Z"), "name" : "Gerbeaud Kávéház", "address" : "Budapest, Vörösmarty tér 7-8", "location" : { "type" : "Point", "coordinates" : [ 47.49693329999999, 19.0502809 ] }, "pictures" : [ "Aap_uED-ou2595rfj3-S4KEWkvFbAnNUe1GNzr-GysZW5bzAMFI28qmKF9VdDH2CvYyhazwVkJMmBm8v_Cgl6SW5CV9U8RLjzMajAE6OBVOwtbbSyOycAKikU5yOEu5MXPLxAZeQuMkTWejA0A0dG-di9uTVTzInLAQ7Nwy-V0VGIfOOlz7d" ] },
{  "google_place_id" : "ChIJ85JGxqHeQUcROo70t-c0JeM", "last_sync" : ISODate("2021-11-19T10:31:27.044Z"), "name" : "Mezzo Music Restaurant", "address" : "Budapest, Maros utca 28", "location" : { "type" : "Point", "coordinates" : [ 47.5052603, 19.0212296 ] }, "pictures" : [ "Aap_uEDBbs2U2F--vuwCs_os6FLevYWRVeuzCfGr41bhJq8cI4TMKjLylme63C4PcIK_8M0ixRhs4TtkSJwZnTNZveO6hmc3QVhto-q0KKEAMTcpnGr56ESq3S1Z_F3Vw4XpbCBfv2QBIfIs9B7tlyaApMLVpOzEdU9wHMXIC2R4SNYiFOgY" ] },
{  "google_place_id" : "ChIJM3Y5yh_cQUcRi-2chMnfGVw", "last_sync" : ISODate("2021-11-19T10:31:27.045Z"), "name" : "Riso Restaurant & Terrace", "address" : "Budapest, Lovas út 41", "location" : { "type" : "Point", "coordinates" : [ 47.5056603, 19.0290262 ] }, "pictures" : [ "Aap_uECifiHmBKAd75FtlgVEe9i2Pn8Sc18TVFX7vS9S1smVa9qHUOih_kIW0h0SPsY_uyRzBU31hW7VJm8wYad0ln2HoNF9EhpVR7TU6s6eFK2CW_noAJQgBZ9itZR-J4l8N3yzKltA4AFJzGkgW206b6pNLe8Gdkk-Ksfw9OOzUFZf2wO8" ] },
{  "google_place_id" : "ChIJVYP_FHncQUcR8FAYVz3LZA4", "last_sync" : ISODate("2021-11-19T10:31:27.047Z"), "name" : "Magyaros Étterem", "address" : "Budapest, Fő utca 10", "location" : { "type" : "Point", "coordinates" : [ 47.4997994, 19.0397555 ] }, "pictures" : [ "Aap_uEArwwMftRCYcjeFRYN_E4xgokWQIPTrtmBAfvoBliaB7zN_FB-zN-FjoxBzJrlT-xm7BQCF2_PnorDMb4rRPa8TwOMPY1nLVNX7851z-hSQLX2CIv8DXXQSP5oaUvZwU7WvvmiBKrRZ4giJuQVENbN8Da4n04voLYPKdsdywxJT3NcI" ] },
{  "google_place_id" : "ChIJwUc67xfcQUcRrFwgAgUHFbE", "last_sync" : ISODate("2021-11-19T10:31:27.048Z"), "name" : "Belgian Brasserie Henri", "address" : "Budapest, Bem rakpart 12", "location" : { "type" : "Point", "coordinates" : [ 47.5016568, 19.0397016 ] }, "pictures" : [ "Aap_uECx77Wpap2Oiym3dGXOnPNKZrsrG2aewlkanpCElTL-Hqdu0qtJRTjuoccsAQItKh6g86kfbHmg7O6i6bIhF_4Q7IK1ecXr1IyeXYL50GFG0SU9NgMikRvRVB1GbJ23V2rRpzEc3_IMTeD9rnkf3BrKcMNzBvGwmYwUYJCLqbcPJQxL" ] },
{  "google_place_id" : "ChIJXYbG8RfcQUcR9pOTQ6qyS10", "last_sync" : ISODate("2021-11-19T10:31:27.049Z"), "name" : "Dunaparti Matróz Kocsma", "address" : "Budapest, Halász utca 1", "location" : { "type" : "Point", "coordinates" : [ 47.5020696, 19.0393614 ] }, "pictures" : [ "Aap_uEBw9vSscni36RzYdzmHil4pQf362YZE-19MwYAKzmAu8ALLhBeww8pxxbvqdSHpOIXBL9Wjw7lWkqCQBI524mq43E7bJEpf-eKf3b9KLueNq2ZjTVASzo--PT9lFhZrJ7pXWGTHY4187DP8B30JtAxC3Ql0iGb9V6L9NXRgWF5L5PkW" ] },
{  "google_place_id" : "ChIJ0yTvOB7cQUcRgUfaTSWWQew", "last_sync" : ISODate("2021-11-19T10:31:27.050Z"), "name" : "Arany Kaviár Étterem", "address" : "Budapest, Ostrom utca 19", "location" : { "type" : "Point", "coordinates" : [ 47.5064327, 19.0285175 ] }, "pictures" : [ "Aap_uEA1946l-Puqe_BP50cOOMT-Ac3GS3iCngyzOqyqikfm42eWBiMMwYqeN8B1gH_hxBBEthcl67pWPj6dWZK4XZ5Zw4DQ45RdBwYkForY9g41qPcKtzH15mJP6BICywXEc41fsG3481WXSwpvkcNC1pyR3kaWDnRGXR4xN8f-vnu6gKA-" ] },
{  "google_place_id" : "ChIJxw3Fo6DeQUcReG_xX5jNE5k", "last_sync" : ISODate("2021-11-19T10:31:27.051Z"), "name" : "Burger King", "address" : "Budapest, Széna tér 7", "location" : { "type" : "Point", "coordinates" : [ 47.5073034, 19.0269227 ] }, "pictures" : [ "Aap_uEA-wF8Lrcr0fsI_clAHwEWoRxTxjUCCfAaFTsAvdBMAAgSVEYSR38_WQ7o9y0R2TLIg8puM8QI3sTQWHbtwOinEfzMt0NrbBEZQ9jhQEJmfsQWzmHzT-7GDG5v8gokd1GgQtwg2ZYConPHa2KQGF_Hx-_yfAPsSufYZ_hx5zseNNwUR" ] },
{  "google_place_id" : "ChIJLULxtL7eQUcR5YZibYLyB0E", "last_sync" : ISODate("2021-11-19T10:31:27.053Z"), "name" : "Lugas Vendéglő", "address" : "Budapest, Szilágyi Erzsébet fasor 77", "location" : { "type" : "Point", "coordinates" : [ 47.5116911, 19.0067253 ] }, "pictures" : [ "Aap_uECNOX-01_Uex1iAJTvqPU70NUr-ngp7hdS9zISmrLdkSAnz7ccA4VXcUjjEJVwvvtAxhSV2kqa92F_N6bMJGAYGkn5B9-7cRr8Ue5-S_UxNflCfNTDYHU1oTbKdEyZcG2hudHolSm3QmG_xXhYefu_WHHSHJ-X6y2R-6xbOhOARvEnW" ] },
];
db.places.insertMany(places);

rubin = db.places.findOne({"google_place_id": "ChIJa6hBF8XdQUcROxJNKIQJBRg"})
artbistrobar = db.places.findOne({"google_place_id": "ChIJt2RniRfcQUcRpiij772lJOw"})
larus = db.places.findOne({"google_place_id": "ChIJ_UtEmincQUcRfmrMihpcE90"})
gerbeaud = db.places.findOne({"google_place_id": "ChIJeQACh0DcQUcRVO6JctVQ5-g"})
magyaros = db.places.findOne({"google_place_id": "ChIJVYP_FHncQUcR8FAYVz3LZA4"})
burgerking = db.places.findOne({"google_place_id": "ChIJxw3Fo6DeQUcReG_xX5jNE5k"})
dunaparti = db.places.findOne({"google_place_id": "ChIJXYbG8RfcQUcR9pOTQ6qyS10"})

/**
 * Initialize reviews
 */

db.createCollection("reviews");
reviews = [
    {
        "user_id": pista1._id,
        "place_id": rubin._id,
        "rating": 3,
        "text": "Kurva jó hely"
    },
    {
        "user_id": pista2._id,
        "place_id": larus._id,
        "rating": 2,
        "text": "Túl zajos hely"
    },
    {
        "user_id": goldschmidt._id,
        "place_id": magyaros._id,
        "rating": 4,
        "text": "public static void main(String[] args) {\nSystem.out.println(\"Jó kaja\");\n}"
    },
    {
        "user_id": neumann._id,
        "place_id": gerbeaud._id,
        "rating": 5,
        "text": "Great food and service"
    },
    {
        "user_id": newton._id,
        "place_id": artbistrobar._id,
        "rating": 5,
        "text": "Nice place, quiet music"
    },
    {
        "user_id": newton._id,
        "place_id": burgerking._id,
        "rating": 3,
        "text": "Too fatty burgers. :("
    },
    {
        "user_id": putin._id,
        "place_id": burgerking._id,
        "rating": 1,
        "text": "blyat"
    }
];
db.reviews.insertMany(reviews);