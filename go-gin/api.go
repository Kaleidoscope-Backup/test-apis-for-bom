package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

type User struct {
	ID    string `json:"id"`
	Name  string `json:"name"`
	Email string `json:"email"`
}

var users = []User{
	{ID: "1", Name: "John Doe", Email: "john@example.com"},
	{ID: "2", Name: "Jane Smith", Email: "jane@example.com"},
}

func main() {
	router := gin.Default()

	// API Title: User Management API

	// Get all users
	router.GET("/users", func(c *gin.Context) {
		c.JSON(http.StatusOK, users)
	})

	// Get user by ID
	router.GET("/users/:id", func(c *gin.Context) {
		id := c.Param("id")
		for _, user := range users {
			if user.ID == id {
				c.JSON(http.StatusOK, user)
				return
			}
		}
		c.JSON(http.StatusNotFound, gin.H{"message": "User not found"})
	})

	// Create a new user
	router.POST("/users", func(c *gin.Context) {
		var newUser User
		if err := c.ShouldBindJSON(&newUser); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		users = append(users, newUser)
		c.JSON(http.StatusCreated, newUser)
	})

	// Update an existing user
	router.PUT("/users/:id", func(c *gin.Context) {
		id := c.Param("id")
		var updatedUser User
		if err := c.ShouldBindJSON(&updatedUser); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		for i, user := range users {
			if user.ID == id {
				users[i] = updatedUser
				c.JSON(http.StatusOK, updatedUser)
				return
			}
		}
		c.JSON(http.StatusNotFound, gin.H{"message": "User not found"})
	})

	// Delete a user
	router.DELETE("/users/:id", func(c *gin.Context) {
		id := c.Param("id")
		for i, user := range users {
			if user.ID == id {
				users = append(users[:i], users[i+1:]...)
				c.JSON(http.StatusOK, gin.H{"message": "User deleted"})
				return
			}
		}
		c.JSON(http.StatusNotFound, gin.H{"message": "User not found"})
	})

	// Start the server
	router.Run(":8080")
}
