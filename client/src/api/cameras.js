import superagent from 'superagent';

export async function getCameraListing() {
    return superagent.get('/api/cameras')
}