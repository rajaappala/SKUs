<template>
  <div class="wrapper">
    <b-container class="bv-example-row">
      <form ref="form" @submit.stop.prevent="getSKUs">
        <b-form-group
          label="Location"
          :state="locationState"
          label-for="location-input"
          invalid-feedback="Location is required"
        >
          <b-form-input
            id="location-input"
            v-model="skuFilters.location"
            :state="locationState"
            required
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          label="Department"
          label-for="department-input"
          :state="deptState"
          invalid-feedback="Department is required"
        >
          <b-form-input
            id="department-input"
            v-model="skuFilters.department"
            :state="deptState"
            required
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          label="Category"
          label-for="category-input"
          :state="catState"
          invalid-feedback="Category is required"
        >
          <b-form-input
            id="category-input"
            v-model="skuFilters.category"
            :state="catState"
            required
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          label="Subcategory"
          label-for="subcategory-input"
          :state="subcatState"
          invalid-feedback="Subcategory is required"
        >
          <b-form-input
            id="subcategory-input"
            v-model="skuFilters.subcategory"
            :state="subcatState"
            required
          >
          </b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="default">Reset</b-button>
      </form>
      <b-card class="mt-3" header="Filtered SKUs">
        <b-table striped hover :items="skus"></b-table>
      </b-card>
    </b-container>
  </div>
</template>
<script>
import { mapGetters, mapActions, mapMutations } from "vuex";
export default {
  name: "LocationComponent",
  data() {
    return {
      skuFilters: {},
      locationState: null,
      deptState: null,
      catState: null,
      subcatState: null,
    };
  },
  computed: {
    ...mapGetters({
      skus: "getSKUs",
    }),
  },
  created() {
    this.set_breadcrumb("Stock Kepping Units");
  },
  methods: {
    ...mapMutations({
      set_breadcrumb: "set_breadcrumb",
    }),
    ...mapActions({
      get_skudata: "get_skudata",
    }),
    checkFormValidity() {
      const valid = this.$refs.form.checkValidity();
      this.locationState = this.skuFilters.location ? true : false;
      this.deptState = this.skuFilters.department ? true : false;
      this.catState = this.skuFilters.category ? true : false;
      this.subcatState = this.skuFilters.subcategory ? true : false;
      return valid;
    },
    getSKUs: function () {
      if (!this.checkFormValidity()) {
        return;
      }
      this.get_skudata(this.skuFilters).then(() => {
        console.log("SKUs filtered");
      });
    },
  },
};
</script>