import axios from 'axios';
import { API_BASE_URL } from '../config';

const recommendationApi = {
  getRecommendations: async (params) => {
    const response = await axios.post(`${API_BASE_URL}/recommend/recommendations/`, params);
    return response.data;
  },

  getTaskStatus: async (taskId) => {
    const response = await axios.get(`${API_BASE_URL}/recommend/tasks/${taskId}/`);
    return response.data;
  },

  getUserPreferences: async () => {
    const response = await axios.get(`${API_BASE_URL}/recommend/preferences/`);
    return response.data;
  },

  updateUserPreferences: async (preferences) => {
    const response = await axios.post(`${API_BASE_URL}/recommend/preferences/`, preferences);
    return response.data;
  },

  getSongFeatures: async (songId) => {
    const response = await axios.get(`${API_BASE_URL}/recommend/song-features/?song_id=${songId}`);
    return response.data;
  },

  getUserSimilarities: async () => {
    const response = await axios.get(`${API_BASE_URL}/recommend/user-similarities/`);
    return response.data;
  },

  getSongSimilarities: async (songId) => {
    const response = await axios.get(`${API_BASE_URL}/recommend/song-similarities/?song_id=${songId}`);
    return response.data;
  },

  calculateUserSimilarities: async () => {
    const response = await axios.post(`${API_BASE_URL}/recommend/user-similarities/calculate/`);
    return response.data;
  },

  calculateSongSimilarities: async () => {
    const response = await axios.post(`${API_BASE_URL}/recommend/song-similarities/calculate/`);
    return response.data;
  },
};

export default recommendationApi; 