package com.face.config;//package com.face.config;
//
//
//
//import lombok.extern.slf4j.Slf4j;
//import org.springframework.context.annotation.Bean;
//import org.springframework.context.annotation.Configuration;
//import org.springframework.stereotype.Component;
//import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
//import org.springframework.web.servlet.config.annotation.WebMvcConfigurationSupport;
//import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
//import springfox.documentation.builders.ApiInfoBuilder;
//import springfox.documentation.builders.PathSelectors;
//import springfox.documentation.builders.RequestHandlerSelectors;
//import springfox.documentation.service.ApiInfo;
//import springfox.documentation.spi.DocumentationType;
//import springfox.documentation.spring.web.plugins.Docket;
//import springfox.documentation.swagger2.annotations.EnableSwagger2;
//
//@Configuration
//@Component
//@Slf4j
//@EnableSwagger2
//public class SwaggerConfig extends WebMvcConfigurationSupport {
//
//    @Bean
//    public Docket createRestApi() {
//        return new Docket(DocumentationType.SWAGGER_2)
//                .apiInfo(apiInfo())
//                //是否开启 (true 开启  false隐藏。生产环境建议隐藏)
//                //.enable(false)
//                .select()
//                //扫描的路径包,设置basePackage会将包下的所有被@Api标记类的所有方法作为api
//                .apis(RequestHandlerSelectors.basePackage("com.face.controller"))
//                //指定路径处理PathSelectors.any()代表所有的路径
//                .paths(PathSelectors.any())
//                .build();
//    }
//
//    private ApiInfo apiInfo() {
//        return new ApiInfoBuilder()
//                //设置文档标题(API名称)
//                .title("SpringBoot中使用Swagger2接口规范")
//                //文档描述
//                .description("接口说明")
//                //服务条款URL
//                .termsOfServiceUrl("http://localhost:8089/")
//                //版本号
//                .version("1.0.0")
//                .build();
//    }
//
////        protected void addResourceHandlers(ResourceHandlerRegistry registry) {
////        log.info("开始进行静态资源映射");
////        registry.addResourceHandler("/doc.html").addResourceLocations("classpath:/META-INF/resources/");
////        registry.addResourceHandler("/webjars/**").addResourceLocations("classpath:/META-INF/resources/webjars/");
//
//
//
//}

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurationSupport;
import springfox.documentation.builders.ApiInfoBuilder;
import springfox.documentation.builders.PathSelectors;
import springfox.documentation.builders.RequestHandlerSelectors;
import springfox.documentation.service.ApiInfo;
import springfox.documentation.spi.DocumentationType;
import springfox.documentation.spring.web.plugins.Docket;
import springfox.documentation.swagger2.annotations.EnableSwagger2;

/**
 1. swagger配置类
 */
@Configuration
@EnableSwagger2
public class SwaggerConfig extends WebMvcConfigurationSupport {
    @Bean
    public Docket createRestApi() {
        return new Docket(DocumentationType.SWAGGER_2)
                .apiInfo(apiInfo())
                //是否开启 (true 开启  false隐藏。生产环境建议隐藏)
                //.enable(false)
                .select()
                //扫描的路径包,设置basePackage会将包下的所有被@Api标记类的所有方法作为api
                .apis(RequestHandlerSelectors.basePackage("com.face.controller"))
                //指定路径处理PathSelectors.any()代表所有的路径
                .paths(PathSelectors.any())
                .build();
    }

    private ApiInfo apiInfo() {
        return new ApiInfoBuilder()
                //设置文档标题(API名称)
                .title("SpringBoot中使用Swagger2接口规范")
                //文档描述
                .description("接口说明")
                //服务条款URL
                .termsOfServiceUrl("http://localhost:8089/")
                //版本号
                .version("1.0.0")
                .build();
    }

    /***
     * 配置静态资源访问拦截
     * @param registry
     */
    public void addResourceHandlers(ResourceHandlerRegistry registry){
        registry.addResourceHandler("swagger-ui.html")
                .addResourceLocations("classpath:/META-INF/resources/");
        registry.addResourceHandler("/webjars/**")
                .addResourceLocations("classpath:/META-INF/resources/webjars/");
    }

}

//swagger访问网站
//http://localhost:8089/swagger-ui.html