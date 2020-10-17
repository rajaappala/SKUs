<template>
  <div class="wrapper">
    <b-container class="bv-example-row">
      <b-row>
        <b-col cols="2">
          <b-sidebar
            id="sidebar-no-header"
            bg-variant="dark"
            text-variant="light"
            sidebar-class="border-right border-danger"
            title="SKU"
            aria-labelledby="sidebar-no-header-title"
            width="250px"
            visible
            shadow
          >
            <template>
              <nav
                class="navbar navbar-vertical fixed-left navbar-expand-md navbar-light"
                id="sidenav-main"
              >
                <div>
                  <b-nav vertical>
                    <b-nav-item to="/locations">Locations</b-nav-item>
                    <b-nav-item to="/departments">Departments</b-nav-item>
                    <b-nav-item to="/categories">Categories</b-nav-item>
                    <b-nav-item to="/subcategories">Subcategories</b-nav-item>
                    <b-nav-item to="/skus">SKUs</b-nav-item>
                  </b-nav>
                </div>
              </nav>
            </template>
            <template v-slot:footer>
              <div
                class="d-flex bg-dark text-light align-items-center px-3 py-2"
              >
                <b-nav vertical>
                  <b-nav-item @click="logout">Sign out</b-nav-item>
                </b-nav>
              </div>
            </template>
          </b-sidebar>
        </b-col>
        <b-col cols="10">
          <div class="main-content md-10 mt-5">
            <div>
              <b-breadcrumb :items="breadcrumbItems"></b-breadcrumb>
              <!-- content here -->
              <router-view></router-view>
            </div>
          </div>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>
<script>
import { mapGetters } from 'vuex'
export default {
  props: {},
  computed: {
    ...mapGetters({
      breadcrumbItems: "getbreadcrumbItems",
    }),
  },
  methods: {
    logout: function () {
      this.$store.dispatch("logout").then(() => {
        this.$router.push("/login");
      });
    },
  },
};
</script>
<style lang="scss">
</style>
