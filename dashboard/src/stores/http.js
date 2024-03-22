import axios from 'axios';
import qs from 'qs';
import { defineStore } from 'pinia';

export const useHttpStore = defineStore('createRequest()', () => {
  const baseURL =
    location.origin.indexOf('us-east-1') !== -1
      ? 'https://api.disaster-us-east-1.thienlinh.link'
      : 'https://api.disaster-ap-southeast-1.thienlinh.link';

  const createRequest = () =>
    axios.create({
      baseURL,
      validateStatus: (status) => {
        return status >= 200 && status < 500;
      }
      // headers: {
      //   Authorization: globalStore.authToken
      // }
    });

  async function find(id, query = {}) {
    return (await createRequest().get(`${id}?${qs.stringify(query)}`)).data;
  }

  async function create(id, payload) {
    return (await createRequest().post(id, payload)).data;
  }

  async function get(id, query) {
    const res = await createRequest().get(
      id + (query ? `?${qs.stringify(query)}` : '')
    );
    if (res.status === 404) return null;
    return res.data;
  }

  async function patch(id, upd) {
    return (await createRequest().patch(id, upd)).data;
  }

  async function remove(id) {
    return (await createRequest().delete(id)).data;
  }

  async function put(...args) {
    return (await createRequest().put(...args)).data;
  }

  return {
    baseURL,
    find,
    create,
    get,
    patch,
    remove,
    put
  };
});
