import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

Vue.use(Vuex);
axios.defaults.baseURL = process.env.VUE_APP_API_BASE_URL

export default new Vuex.Store({
  state: {
    token: localStorage.getItem('access_token') || '',
    locations: [],
    location: {},
    departments: [],
    department: {},
    locationsFordepts: [],
    categories: [],
    category: {},
    deptsForCategory: [],
    subcategories: [],
    subcategory: {},
    catForSubcat: [],
    skus: [],
    infoGraphData: {},
    breadcrumbItems: [],
  },
  mutations: {
    // Auth Mutations 

    auth_request(state) {
      state.status = 'loading'
    },
    auth_success(state, access_token, user) {
      state.status = 'success'
      state.token = access_token
      state.user = user
    },
    auth_error(state) {
      state.status = 'error'
    },
    logout(state) {
      state.status = ''
      state.token = ''
    },

    // Location Mutations

    set_location(state, location) {
      state.location = location
    },
    set_locations(state, locations) {
      state.locations = locations
    },
    add_location(state, location) {
      state.locations.unshift(location)
    },

    // Department Mutations

    set_department(state, department) {
      state.department = department
    },
    set_departments(state, data) {
      state.departments = data.results.departments
      state.locationsFordepts = data.results.locations
    },
    add_department(state, department) {
      state.departments.unshift(department)
    },

    // Category Mutations

    set_category(state, category) {
      state.category = category
    },
    set_categories(state, data) {
      state.categories = data.results.categories
      state.deptsForCategory = data.results.departments
    },
    add_category(state, category) {
      state.categories.unshift(category)
    },

    // Subcategory Mutations

    set_subcategory(state, subcategory) {
      state.subcategory = subcategory
    },
    set_subcategories(state, data) {
      state.subcategories = data.results.subcategories
      state.catForSubcat = data.results.categories
    },
    add_subcategory(state, subcategory) {
      state.subcategories.unshift(subcategory)
    },

    set_skus(state, data) {
      state.skus = data
    },

    set_breadcrumb(state, breadcrumb) {
      state.breadcrumbItems = [breadcrumb]
    },

    set_infograph(state, infograph){
      state.infoGraphData = infograph
    }
  },
  actions: {

    // Auth Actions

    login({ commit }, user) {
      return new Promise((resolve, reject) => {
        commit('auth_request')
        axios({ url: '/token/', data: user, method: 'POST' })
          .then(resp => {
            const access_token = resp.data.access
            const refresh_token = resp.data.refresh
            localStorage.setItem('access_token', access_token)
            localStorage.setItem('refresh', refresh_token)
            axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`

            commit('auth_success', access_token, user)
            resolve(resp)
          })
          .catch(err => {
            commit('auth_error')
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')
            reject(err)
          })
      })
    },
    logout({ commit }) {
      return new Promise((resolve, reject) => {
        commit('logout')
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        delete axios.defaults.headers.common['Authorization']
        resolve()
      })
    },

    // Location Actions

    get_locations({ commit }, pageOffset=0) {
      return new Promise((resolve, reject) => {
        axios({ url: `/location/?offset=${pageOffset}`, method: 'GET' })
          .then(resp => {
            commit('set_locations', resp.data.results)
            resolve(resp)
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    create_location({ commit }, location) {
      return new Promise((resolve, reject) => {
        axios({ url: '/location/', data: location, method: 'POST' })
          .then(resp => {
            commit('add_location', resp.data)
            resolve(resp)
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    update_location({ commit }, location) {
      return new Promise((resolve, reject) => {
        axios({ url: `/location/${location.id}/`, data: location, method: 'PUT' })
          .then(resp => {
            this.dispatch('get_locations')
            resolve(resp)
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    delete_location({ commit }, locationID) {
      return new Promise((resolve, reject) => {
        axios({ url: `/location/${locationID}/`, method: 'DELETE' })
          .then(resp => {
            this.dispatch('get_locations')
            resolve(resp)
          })
          .catch(err => {
            reject(err)
          })
      })
    },

    // Department Actions

    get_departments({ commit }, pageOffset=0) {
      return new Promise((resolve, reject) => {
        axios({ url: `/department/?offset=${pageOffset}`, method: 'GET' })
          .then(resp => {
            commit('set_departments', resp.data)
            resolve(resp)
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    create_department({ commit }, department) {
      return new Promise((resolve, reject) => {
        axios({ url: '/department/', data: department, method: 'POST' })
          .then(resp => {
            commit('add_department', resp.data)
            resolve(resp)
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    update_department({ commit }, department) {
      return new Promise((resolve, reject) => {
        axios({ url: `/department/${department.id}/`, data: department, method: 'PUT' })
          .then(resp => {
            this.dispatch('get_departments')
            resolve(resp)
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    delete_department({ commit }, departmentID) {
      return new Promise((resolve, reject) => {
        axios({ url: `/department/${departmentID}/`, method: 'DELETE' })
          .then(resp => {
            this.dispatch('get_departments')
            resolve(resp)
          })
          .catch(err => {
            reject(err)
          })
      })
    },


    // Category Actions

    get_categories({ commit }, pageOffset=0) {
      return new Promise((resolve, reject) => {
        axios({ url: `/category/?offset=${pageOffset}`, method: 'GET' })
          .then(resp => {
            commit('set_categories', resp.data)
            resolve(resp)
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    create_category({ commit }, category) {
      return new Promise((resolve, reject) => {
        axios({ url: '/category/', data: category, method: 'POST' })
          .then(resp => {
            commit('add_category', resp.data)
            resolve(resp)
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    update_category({ commit }, category) {
      return new Promise((resolve, reject) => {
        axios({ url: `/category/${category.id}/`, data: category, method: 'PUT' })
          .then(resp => {
            this.dispatch('get_categories')
            resolve(resp)
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    delete_category({ commit }, categoryID) {
      return new Promise((resolve, reject) => {
        axios({ url: `/category/${categoryID}/`, method: 'DELETE' })
          .then(resp => {
            this.dispatch('get_categories')
            resolve(resp)
          })
          .catch(err => {
            reject(err)
          })
      })
    },

    // Subcategory Actions

    get_subcategories({ commit }, pageOffset=0) {
      return new Promise((resolve, reject) => {
        axios({ url: `/subcategory/?offset=${pageOffset}`, method: 'GET' })
          .then(resp => {
            commit('set_subcategories', resp.data)
            resolve(resp)
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    create_subcategory({ commit }, subcategory) {
      return new Promise((resolve, reject) => {
        axios({ url: '/subcategory/', data: subcategory, method: 'POST' })
          .then(resp => {
            commit('add_subcategory', resp.data)
            resolve(resp)
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    update_subcategory({ commit }, subcategory) {
      return new Promise((resolve, reject) => {
        axios({ url: `/subcategory/${subcategory.id}/`, data: subcategory, method: 'PUT' })
          .then(resp => {
            this.dispatch('get_subcategories')
            resolve(resp)
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    delete_subcategory({ commit }, subcategoryID) {
      return new Promise((resolve, reject) => {
        axios({ url: `/subcategory/${subcategoryID}/`, method: 'DELETE' })
          .then(resp => {
            this.dispatch('get_subcategories')
            resolve(resp)
          })
          .catch(err => {
            reject(err)
          })
      })
    },

    //SKU Action
    get_skudata({ commit }, data) {
      return new Promise((resolve, reject) => {
        axios({ url: `/sku?location=${data.location}&department=${data.department}&category=${data.category}&subcategory=${data.subcategory}`, method: 'GET' })
          .then(resp => {
            commit('set_skus', resp.data)
            resolve(resp)
          })
          .catch(err => {
            reject(err)
          })
      });
    },

    //InfoGraph Action
    get_locations_for_infograph({ commit }) {
      return new Promise((resolve, reject) => {
        axios({ url: `/infograph/`, method: 'GET' })
          .then(resp => {
            resolve(resp)
          })
          .catch(err => {
            reject(err)
          })
      });
    },

    get_infograph({ commit }, locationID) {
      return new Promise((resolve, reject) => {
        axios({ url: `/infograph/${locationID}`, method: 'GET' })
          .then(resp => {
            commit("set_infograph", resp.data)
            resolve(resp)
          })
          .catch(err => {
            reject(err)
          })
      });
    },
  },
  getters: {
    isLoggedIn: state => !!state.token,
    authStatus: state => state.status,
    getLocation: state => state.location,
    getLocations: state => state.locations,
    getDept: state => state.department,
    getDepartments: state => state.departments,
    getLocationsFordepartment: state => state.locationsFordepts,
    getCategory: state => state.category,
    getCategories: state => state.categories,
    getDeptsForCategory: state => state.deptsForCategory,
    getSubcategory: state => state.subcategory,
    getSubcategories: state => state.subcategories,
    getCatForSubcat: state => state.catForSubcat,
    getSKUs: state => state.skus,
    getbreadcrumbItems: state => state.breadcrumbItems,
    getInfoGraphData: state => state.infoGraphData,
  },
  modules: {}
});
