import { openDB } from 'idb'

const dbPromise = openDB('sistemaapp-db', 1, {
  upgrade(db) {
    if (!db.objectStoreNames.contains('offline_points')) {
      db.createObjectStore('offline_points', { keyPath: 'id', autoIncrement: true })
    }
  },
})

export const addOfflinePoint = async (point) => {
  const db = await dbPromise
  await db.add('offline_points', point)
}

export const getOfflinePoints = async () => {
  const db = await dbPromise
  return await db.getAll('offline_points')
}

export const clearOfflinePoints = async () => {
  const db = await dbPromise
  await db.clear('offline_points')
}
