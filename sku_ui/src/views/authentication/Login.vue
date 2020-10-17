<template>
  <div>
    <!-- Header -->
    <div class="header bg-gradient-success py-7 py-lg-8 pt-lg-9">
      <b-container>
        <div class="header-body text-center mb-7">
          <b-row class="justify-content-center">
            <b-col xl="5" lg="6" md="8" class="px-5">
              <h1 class="text-white">Welcome!</h1>
            </b-col>
          </b-row>
        </div>
      </b-container>
    </div>
    <!-- Page content -->
    <b-container class="mt-8 pb-5">
      <b-row class="justify-content-center">
        <b-col lg="5" md="7">
          <b-card no-body class="bg-secondary border-0 mb-0">
            <b-card-body class="px-lg-5 py-lg-5">
              <div class="text-center text-muted mb-4">
                <small>Or sign in with credentials</small>
              </div>
                <b-form role="form" @submit.prevent="login" method='POST'>
                  <b-input alternative
                              class="mb-3"
                              name="username"
                              :rules="{required: true, username: true}"
                              placeholder="Username"
                              v-model="model.username">
                  </b-input>

                  <b-input alternative
                              class="mb-3"
                              name="Password"
                              :rules="{required: true, min: 6}"
                              type="password"
                              placeholder="Password"
                              v-model="model.password">
                  </b-input>
                  <div class="text-center">
                    <b-button type="primary" native-type="submit" class="my-4">Sign in</b-button>
                  </div>
                </b-form>
            </b-card-body>
          </b-card>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>
<script>
  export default {
    data() {
      return {
        model: {
          username: '',
          password: '',
        }
      };
    },
    methods: {
      login: function () {
        let username = this.model.username
        let password = this.model.password
        this.$store.dispatch('login', { username, password })
       .then(() => this.$router.push('/'))
       .catch(err => console.log(err))
      }
    }
  };
</script>
