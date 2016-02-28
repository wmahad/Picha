'use strict'
app.factory('MainFactory', function ($resource) {
	return {
        IMage: $resource("api/image/", {}, {
            getImage:{
                method: 'GET',
                isArray: false
            }
        },{
            stripTrailingSlashes: false
        }),
        ModifyImage: $resource("api/modify_photo/", {}, {
            DeleteImage:{
                method: 'DELETE'
            },
            getImageEffects: {
                method: 'GET',
                isArray: false
            }
        },{
            stripTrailingSlashes: false
        }),
        Text: $resource("api/text/", {}, {
            DrawText:{
                method: 'GET',
                isArray: false
            }
        },{
            stripTrailingSlashes: false
        }),
        ImageEffect: $resource("api/imageeffects/", {}, { 
            saveImageEffct:{
                method: 'POST'
            },
            getImageEffcts:{
                method: 'GET',
                isArray: true
            }
        },{
            stripTrailingSlashes: false
        }),
        Enhancement: $resource("api/enhancement/", {}, {
            getEnhancement:{
                method: 'GET',
                isArray: false
            }
        },{
            stripTrailingSlashes: false
        }),
        Rotate: $resource("api/degree/", {}, {
            rotate:{
                method: 'GET',
                isArray: false
            }
        },{
            stripTrailingSlashes: false
        }),

        Filters: $resource("api/filters/", {}, {
            getAllImageFilters: {
                method: 'GET',
                isArray: false
            }
        },{
            stripTrailingSlashes: false
        }),

        Reset: $resource("api/reset/", {}, {
            resetEffects: {
                method: 'GET',
                isArray: false
            }
        },{
            stripTrailingSlashes: false
        })
    };
})