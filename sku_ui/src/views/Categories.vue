<template>
  <div class="mt-3">
    <b-alert :variant="alert.variant" :show="alert.show">{{
      alert.message
    }}</b-alert>
    <div class="float-right pt-3 pb-3">
      <b-button type="button" variant="primary" v-b-modal.category-modal>
        Add Category</b-button
      >
    </div>
    <b-table striped hover :items="categories" :fields="fields">
      <template v-slot:cell(department)="row">
        <span>{{ row.item.department }}</span>
      </template>
      <template v-slot:cell(actions)="row">
        <b-button
          @click="editCategory(row.item, row.index, $event.target)"
          class="mr-1"
          size="sm"
          variant="secondary"
        >
          Edit
        </b-button>
        <b-button
          variant="info"
          size="sm"
          class="mr-1"
          @click="row.toggleDetails"
        >
          {{ row.detailsShowing ? "Hide" : "Show" }} Details
        </b-button>
        <b-button
          @click="deleteCategory(row.item, row.index, $event.target)"
          size="sm"
          variant="danger"
        >
          Delete
        </b-button>
      </template>

      <template v-slot:row-details="row">
        <b-card>
          <ul>
            <li v-for="(value, key) in row.item" :key="key">
              {{ key }}: {{ value }}
            </li>
          </ul>
        </b-card>
      </template>
    </b-table>
    <b-modal
      id="category-modal"
      ref="modal"
      :title="catModal.title"
      @show="resetModal"
      @hidden="resetModal"
      @ok="handleOk"
    >
      <form ref="form" @submit.stop.prevent="handleSubmit">
        <b-form-group
          label="Name"
          :state="nameState"
          label-for="name-input"
          invalid-feedback="Name is required"
        >
          <b-form-input
            id="name-input"
            v-model="getCategory.name"
            :state="nameState"
            required
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          label="Department"
          label-for="department-input"
          :state="departmentState"
          invalid-feedback="Department is required"
        >
          <b-form-select
            id="department-input"
            v-model="getCategory.department"
            :options="getDeptsForCategory"
          ></b-form-select>
        </b-form-group>
      </form>
    </b-modal>
  </div>
</template>

<script>
import { mapGetters, mapActions, mapMutations } from "vuex";
import _ from "lodash";
export default {
  name: "CategoryComponent",
  data() {
    return {
      newCategory: {},
      nameState: null,
      departmentState: null,
      alert: {
        show: false,
        message: "",
        variant: "",
      },
      catModal: {
        title: "Add Category",
      },
      fields: ["id", "name", "department", "user", "last_modified", "actions"],
    };
  },
  computed: {
    ...mapGetters({
      categories: "getCategories",
      getCategory: "getCategory",
      getDeptsForCategory: "getDeptsForCategory",
    }),
  },
  created() {
    this.get_categories();
    this.set_breadcrumb("Categories");
  },
  methods: {
    ...mapMutations({
      set_breadcrumb: "set_breadcrumb",
      set_category: "set_category",
    }),
    ...mapActions({
      get_categories: "get_categories",
      create_category: "create_category",
      update_category: "update_category",
      delete_category: "delete_category",
    }),
    checkFormValidity() {
      const valid = this.$refs.form.checkValidity();
      this.nameState = this.getCategory.name ? true : false;
      this.departmentState = this.getCategory.department ? true : false;
      return valid;
    },
    resetModal() {
      this.nameState = null;
      this.departmentState = null;
    },
    handleOk(bvModalEvt) {
      // Prevent modal from closing
      bvModalEvt.preventDefault();
      // Trigger submit handler
      this.handleSubmit();
    },
    handleSubmit() {
      // Exit when the form isn't valid
      if (!this.checkFormValidity()) {
        return;
      }
      if (this.getCategory.id) {
        this.update_category(this.getCategory).then(() => {
          this.alert.message = "Category updated successfully";
          this.alert.variant = "success";
          this.alert.show = true;
          this.$bvModal.hide("category-modal");
          this.set_category({});
        });
      } else {
        this.create_category(this.getCategory).then(() => {
          this.$bvModal.hide("category-modal");
          this.set_category({});
          this.alert.message = "Category created successfully";
          this.alert.variant = "success";
          this.alert.show = true;
        });
      }
    },
    editCategory(item, index, event) {
      this.newCategory.id = item.id;
      this.newCategory.name = item.name;
      this.newCategory.department = _.find(this.getDeptsForCategory, (val) => {
        if (val.text == item.department) return val;
      }).value;
      this.catModal.titel = `Edit ${item.name}`;
      this.set_category(this.newCategory);
      this.$bvModal.show("category-modal");
    },
    deleteCategory(item, index, event) {
      this.$bvModal
        .msgBoxConfirm(`Please confirm that you want to delete ${item.name}.`, {
          title: "Please Confirm",
          size: "sm",
          buttonSize: "sm",
          okVariant: "danger",
          okTitle: "YES",
          cancelTitle: "NO",
          footerClass: "p-2",
          hideHeaderClose: false,
          centered: true,
        })
        .then((value) => {
          this.delete_category(item.id).then(() => {
            this.alert.message = "Category deleted successfully";
            this.alert.variant = "success";
            this.alert.show = true;
          });
        })
        .catch((err) => {
          // An error occurred
        });
    },
  },
};
</script>