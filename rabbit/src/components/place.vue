<template>
  <div class="form-group">
    <label for="inputEmail3" class="col-xs-offset-1 col-xs-2 control-label yzj-size-16">
      <span class="text-warning size-18">
        *
      </span>
      所在城市
    </label>
    <div class="col-xs-3 clear-right">
      <select class="form-control select-control" id="address_state" v-model="province">
        <option v-for="option in provinces" v-bind:value="option">
          {[ option.name ]}
        </option>
      </select>
    </div>
    <div class="col-xs-3">
      <select class="form-control select-control" name="city_id" v-model="city_id">
        <option v-for="option in cities" v-bind:value="option.address_id" >
          {[ option.name ]}
        </option>
      </select>
    </div>
  </div>
  <div class="form-group form-error" for="city_id">
    <div class="col-xs-offset-3 col-xs-9 text-warning yzj-size-14">
      <span class="glyphicon glyphicon-exclamation-sign yzj-right-distance10"
      aria-hidden="true"></span>
      城市是必选字段
    </div>
  </div>
</template>
<script>
import $ from 'jquery'
export default {
  created () {
    let _self = this
    console.log('created from lace', this.city_id)
    $.getJSON('/api/address', {address_id: 0, t: 'all'}, (data) => {
      _self.places = data.addresses
      _self.provinces = _self.getPlacesByParentId(1, _self.places)
      _self.setPlace(_self.city_id)
    })
  },
  data () {
    return {
      province: {},
      provinces: [],
      city: {},
      cities: [],
      places: []
    }
  },
  methods: {
    updateCity (option) {
    },
    getPlacesByParentId (id, places) {
      let results = []
      for (let i = 0; i < places.length; i++) {
        if (places[i].pid === id) {
          results.push(places[i])
        }
      }
      return results
    },
    getPlaceById (id, places) {
      for (let i = 0; i < places.length; i++) {
        if (places[i].address_id === id) {
          return places[i]
        }
      }
    },
    setPlace (value) {
      console.log(value, 'place created')
      if (value) {
        this.city = this.getPlaceById(value, this.places)
        console.log(this.city, 'place created city')
        this.province = this.getPlaceById(this.city.pid, this.places)
        console.log(this.province, 'place created province')
        this.cities = this.getPlacesByParentId(this.province.address_id, this.places)
      } else {
        this.province = this.provinces[0]
        this.cities = this.getPlacesByParentId(this.province.address_id, this.places)
        this.city = this.cities[0]
      }
    }

  },

  props: ['city_id'],
  watch: {
    province (value) {
      this.cities = this.getPlacesByParentId(value.address_id, this.places)
      this.city = this.cities[0]
    },
    city_id (value) {
      this.setPlace(value)
    }
  }

}
</script>
