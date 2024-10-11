const fs = require('fs')
require('dotenv').config()

async function getMovies() {
    let movies = []
    for (let page = 1; page <= 200; page++) {
        console.log(`Fetching page: ${ page }`)
        const url = `https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=${ page }&sort_by=vote_count.desc`
        const options = {
            method: 'GET',
            headers: {
                accept: 'application/json',
                Authorization: `Bearer ${ process.env.TMDB_API_KEY }`
            }
        }
        const result = await fetch(url, options)
        const payload = await result.json()
        movies = movies.concat(payload.results.map(movie => { 
            return { id: movie.id, title: movie.title, poster_path: movie.poster_path, overview: movie.overview }
        }))
    }
    fs.writeFileSync('movies.json', JSON.stringify(movies))
    console.log(`Wrote ${ movies.length } movies to movies.json`)
}

getMovies()
