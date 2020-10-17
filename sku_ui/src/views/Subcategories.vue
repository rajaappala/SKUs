<template>
  <div class="mt-3">
    <b-alert :variant="alert.variant" :show="alert.show">{{
      alert.message
    }}</b-alert>
    <div class="float-right pt-3 pb-3">
      <b-button type="button" variant="primary" v-b-modal.subcategory-modal>
        Add Subcategory</b-button
      >
    </div>
    <b-table striped hover :items="subcategories" :fields="fields">
      <template v-slot:cell(actions)="row">
        <b-button
          @click="editSubcategory(row.item, row.index, $event.target)"
          class="mr-1"
          size="sm"
        >
          Edit
        </b-button>
        <b-button size="sm" class="mr-1" @click="row.toggleDetails">
          {{ row.detailsShowing ? "Hide" : "Show" }} Details
        </b-button>
        <b-button
          @click="deleteSubcategory(row.item, row.index, $event.target)"
          size="sm"
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
      id="subcategory-modal"
      ref="modal"
      :title="subcatModal.title"
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
            v-model="getSubcategory.name"
            :state="nameState"
            required
          >
          </b-form-input>
        </b-form-group>
        <b-form-group
          label="category"
          label-for="category-input"
          :state="categoryState"
          invalid-feedback="Category is required"
        >
          <b-form-select
            id="category-input"
            v-model="getSubcategory.category"
            :options="getCatForSubcat"
          ></b-form-select>
        </b-form-group>
      </form>
    </b-modal>
  </div>
</template>

<script>
import { mapGetters, mapActions, mapMutations } from "vuex";
export default {
  name: "SubcategoryComponent",
  data() {
    return {
      newSubcategory: {},
      nameState: null,
      categoryState: null,
      alert: {
        show: false,
        message: "",
        variant: "",
      },
      subcatModal: {
        title: "Add Subcategory",
      },
      fields: ["id", "name", "category", "user", "last_modified", "actions"],
    };
  },
  computed: {
    ...mapGetters({
      subcategories: "getSubcategories",
      getSubcategory: "getSubcategory",
      getCatForSubcat: "getCatForSubcat",
    }),
  },
  created() {
    this.get_subcategories();
    this.set_breadcrumb("Subcategories");
  },
  methods: {
    ...mapMutations({
      set_breadcrumb: "set_breadcrumb",
      set_subcategory: "set_subcategory",
    }),
    ...mapActions({
      get_subcategories: "get_subcategories",
      create_subcategory: "create_subcategory",
      update_subcategory: "update_subcategory",
      delete_subcategory: "delete_subcategory",
    }),
    checkFormValidity() {
      const valid = this.$refs.form.checkValidity();
      this.nameState = this.getSubcategory.name ? true : false;
      this.categoryState = this.getSubcategory.category ? true : false;
      return valid;
    },
    resetModal() {
      this.nameState = null;
      this.categoryState = null;
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
      if (this.getSubcategory.id) {
        this.update_subcategory(this.getSubcategory).then(() => {
          this.alert.message = "Subcategory updated successfully";
          this.alert.variant = "success";
          this.alert.show = true;
          this.$bvModal.hide("subcategory-modal");
          this.set_subcategory({});
        });
      } else {
        this.create_subcategory(this.getSubcategory).then(() => {
          this.$bvModal.hide("subcategory-modal");
          this.set_subcategory({});
          this.alert.message = "Subcategory created successfully";
          this.alert.variant = "success";
          this.alert.show = true;
        });
      }
    },
    editSubcategory(item, index, event) {
      this.newSubcategory.id = item.id;
      this.newSubcategory.name = item.name;
      this.newSubcategory.category = item.category;
      this.subcatModal.titel = `Edit ${item.name}`;
      this.set_subcategory(this.newSubcategory);
      this.$bvModal.show("subcategory-modal");
    },
    deleteSubcategory(item, index, event) {
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
          this.delete_subcategory(item.id).then(() => {
            this.alert.message = "Subategory deleted successfully";
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